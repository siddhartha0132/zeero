"""In-memory case store. Each case holds the uploaded documents, the agent conversation and its outputs."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from .documents import Document, guess_doc_type


@dataclass
class Case:
    id: str
    documents: dict[str, Document] = field(default_factory=dict)
    messages: list[dict[str, Any]] = field(default_factory=list)
    plan: list[dict[str, str]] = field(default_factory=list)
    bill_assessment: dict[str, Any] | None = None
    checklist: list[dict[str, str]] | None = None
    drafts: dict[str, dict[str, str]] = field(default_factory=dict)
    verdict: dict[str, Any] | None = None
    busy: bool = False
    _next_doc_number: int = 1

    def add_document(self, filename: str, text: str, doc_type: str | None = None) -> Document:
        doc = Document(
            id=f"doc{self._next_doc_number}", filename=filename, doc_type=doc_type or guess_doc_type(text), text=text
        )
        self._next_doc_number += 1
        self.documents[doc.id] = doc
        return doc

    def reset_analysis(self) -> None:
        self.messages.clear()
        self.plan = []
        self.bill_assessment = None
        self.checklist = None
        self.drafts = {}
        self.verdict = None

    def public_state(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "documents": [
                {"id": doc.id, "filename": doc.filename, "doc_type": doc.doc_type, "characters": len(doc.text)}
                for doc in self.documents.values()
            ],
            "plan": self.plan,
            "bill_assessment": self.bill_assessment,
            "checklist": self.checklist,
            "drafts": list(self.drafts.values()),
            "verdict": self.verdict,
            "busy": self.busy,
            "has_conversation": bool(self.messages),
        }


class CaseStore:
    def __init__(self) -> None:
        self._cases: dict[str, Case] = {}

    def create(self) -> Case:
        case = Case(id=uuid.uuid4().hex[:12])
        self._cases[case.id] = case
        return case

    def get(self, case_id: str) -> Case | None:
        return self._cases.get(case_id)
