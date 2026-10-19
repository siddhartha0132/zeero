"""Turning uploads into searchable text: extraction, document-type guessing, clause chunking and BM25 search."""

from __future__ import annotations

import io
import math
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pypdf import PdfReader
from pypdf.errors import PdfReadError

DOC_TYPES = ("policy", "hospital_bill", "discharge_summary", "rejection_letter", "other")
TEXT_SUFFIXES = {".txt", ".md", ".csv"}
IMAGE_MIME_TYPES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
MAX_CHUNK_CHARS = 1500


class UnsupportedDocument(ValueError):
    pass


@dataclass
class Chunk:
    heading: str
    text: str
    tokens: Counter[str]
    length: int


@dataclass
class Document:
    id: str
    filename: str
    doc_type: str
    text: str
    chunks: list[Chunk] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.chunks:
            self.chunks = chunk_text(self.text)


def extract_text(filename: str, data: bytes) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix == ".pdf":
        try:
            reader = PdfReader(io.BytesIO(data))
            pages = [f"[Page {number}]\n{page.extract_text() or ''}" for number, page in enumerate(reader.pages, start=1)]
        except PdfReadError as exc:
            raise UnsupportedDocument(f"{filename}: could not read this PDF ({exc}).") from exc
        text = "\n\n".join(pages)
        if len(re.sub(r"\[Page \d+\]|\s", "", text)) < 50:
            raise UnsupportedDocument(
                f"{filename} looks like a scanned PDF with no text layer. Upload photos (JPG/PNG) of the pages instead."
            )
        return text
    if suffix in TEXT_SUFFIXES:
        return data.decode("utf-8", errors="replace")
    raise UnsupportedDocument(f"{filename}: unsupported file type. Use PDF, JPG/PNG/WEBP photos, or .txt files.")


# Titles usually say what a document is, so check the top of the page first.
_HEADER_MARKERS = (
    ("rejection_letter", ("repudiation", "rejection of claim", "claim rejection", "denial of claim")),
    ("discharge_summary", ("discharge summary",)),
    ("policy", ("policy wording", "policy schedule", "policy terms and conditions")),
    ("hospital_bill", ("bill", "invoice")),
)
_BODY_KEYWORDS = {
    "rejection_letter": ("repudiat", "regret", "not admissible", "rejected", "denied"),
    "policy": ("sum insured", "waiting period", "exclusion", "moratorium", "definition"),
    "discharge_summary": ("diagnosis", "date of discharge", "past history", "condition at discharge", "presenting complaint"),
    "hospital_bill": ("qty", "rate", "amount", "gross total", "balance", "gst"),
}


def guess_doc_type(text: str) -> str:
    header = text[:600].lower()
    for doc_type, markers in _HEADER_MARKERS:
        if any(marker in header for marker in markers):
            return doc_type
    lowered = text.lower()
    scores = {doc_type: sum(lowered.count(k) for k in keywords) for doc_type, keywords in _BODY_KEYWORDS.items()}
    best = max(scores, key=lambda doc_type: scores[doc_type])
    return best if scores[best] > 0 else "other"


_STOPWORDS = set(
    "a an and are as at be by for from has have in is it of on or shall that the this to under was were which will with".split()
)
_SUFFIXES = ("ation", "ings", "ing", "ies", "ed", "es", "s")


def tokenize(text: str) -> list[str]:
    tokens = []
    for word in re.findall(r"[a-z0-9]+", text.lower()):
        if word in _STOPWORDS:
            continue
        for suffix in _SUFFIXES:
            if word.endswith(suffix) and len(word) - len(suffix) >= 3:
                word = word[: -len(suffix)]
                break
        tokens.append(word)
    return tokens


_SECTION_LINE = re.compile(r"^(SECTION|ANNEXURE|PART|SCHEDULE)\b", re.IGNORECASE)
_CLAUSE_LINE = re.compile(r"^(\d+\.\d+(?:\.\d+)*)\s+(.{0,70})")


def _is_section_heading(line: str) -> bool:
    if _SECTION_LINE.match(line):
        return True
    letters = re.sub(r"[^A-Za-z]", "", line)
    return len(line) <= 90 and len(letters) >= 4 and line == line.upper()


def chunk_text(text: str) -> list[Chunk]:
    """Split into clause-sized chunks, each labelled with its section and clause number for citations."""
    raw_chunks: list[tuple[str, list[str]]] = []
    section = ""
    heading, lines = "", []

    def flush() -> None:
        if any(line.strip() for line in lines):
            raw_chunks.append((heading, lines.copy()))
        lines.clear()

    for line in text.splitlines():
        stripped = line.strip()
        if stripped and _is_section_heading(stripped):
            flush()
            section = stripped
            heading = section
        elif clause := _CLAUSE_LINE.match(stripped):
            flush()
            label = clause.group(2).split(":")[0].strip()
            heading = f"{section} › {clause.group(1)} {label}".strip(" ›")
        lines.append(line)
    flush()

    chunks = []
    for chunk_heading, chunk_lines in raw_chunks:
        body = "\n".join(chunk_lines).strip()
        for start in range(0, len(body), MAX_CHUNK_CHARS):
            piece = body[start : start + MAX_CHUNK_CHARS]
            tokens = tokenize(f"{chunk_heading} {piece}")
            chunks.append(Chunk(heading=chunk_heading, text=piece, tokens=Counter(tokens), length=len(tokens)))
    return chunks


def search_documents(
    documents: list[Document], query: str, doc_type: str | None = None, top_k: int = 5
) -> list[dict[str, Any]]:
    """BM25 over clause chunks — small, dependency-free and good enough for a handful of documents."""
    candidates = [(doc, chunk) for doc in documents for chunk in doc.chunks if doc_type in (None, doc.doc_type)]
    query_terms = set(tokenize(query))
    if not candidates or not query_terms:
        return []

    k1, b = 1.5, 0.75
    count = len(candidates)
    average_length = sum(chunk.length for _, chunk in candidates) / count or 1
    document_frequency: Counter[str] = Counter()
    for _, chunk in candidates:
        document_frequency.update(set(chunk.tokens))

    scored = []
    for doc, chunk in candidates:
        score = 0.0
        for term in query_terms:
            frequency = chunk.tokens.get(term, 0)
            if not frequency:
                continue
            idf = math.log(1 + (count - document_frequency[term] + 0.5) / (document_frequency[term] + 0.5))
            score += idf * frequency * (k1 + 1) / (frequency + k1 * (1 - b + b * chunk.length / average_length))
        if score > 0:
            scored.append((score, doc, chunk))
    scored.sort(key=lambda item: item[0], reverse=True)

    return [
        {
            "doc_id": doc.id,
            "filename": doc.filename,
            "doc_type": doc.doc_type,
            "section": chunk.heading,
            "text": chunk.text,
            "score": round(score, 2),
        }
        for score, doc, chunk in scored[: max(1, min(top_k, 10))]
    ]
