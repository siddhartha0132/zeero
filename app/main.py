from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Optional

import openai
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .agent import kickoff_message, run_agent
from .config import load_settings
from .documents import DOC_TYPES, IMAGE_MIME_TYPES, UnsupportedDocument, extract_text
from .llm import OpenAICompatibleLLM, describe_llm_error
from .store import Case, CaseStore

ROOT = Path(__file__).resolve().parent.parent
SAMPLES_DIR = ROOT / "samples"
STATIC_DIR = ROOT / "static"
MAX_UPLOAD_BYTES = 15 * 1024 * 1024

logger = logging.getLogger("claimsaathi")

settings = load_settings()
app = FastAPI(title="ClaimSaathi")
app.state.store = CaseStore()
app.state.llm = OpenAICompatibleLLM(settings)
app.state.max_agent_steps = settings.max_agent_steps


class RunRequest(BaseModel):
    message: str = ""
    mode: Optional[str] = None  # "appeal" or "pre_claim" starts a fresh analysis; omit for a follow-up message


class DocTypeUpdate(BaseModel):
    doc_type: str


def _get_case(request: Request, case_id: str) -> Case:
    case = request.app.state.store.get(case_id)
    if case is None:
        raise HTTPException(404, "Case not found. Refresh the page to start a new case.")
    return case


def _sse(event: dict[str, Any]) -> str:
    return f"data: {json.dumps(event, ensure_ascii=False)}\n\n"


@app.get("/api/health")
def health(request: Request) -> dict[str, Any]:
    llm = request.app.state.llm
    return {"ok": True, "llm_ready": llm.ready, "model": llm.model_name}


@app.post("/api/cases")
def create_case(request: Request) -> dict[str, Any]:
    return request.app.state.store.create().public_state()


@app.get("/api/cases/{case_id}")
def get_case(case_id: str, request: Request) -> dict[str, Any]:
    return _get_case(request, case_id).public_state()


@app.post("/api/cases/{case_id}/documents")
async def upload_documents(case_id: str, request: Request, files: list[UploadFile] = File(...)) -> dict[str, Any]:
    case = _get_case(request, case_id)
    llm = request.app.state.llm
    added, errors = [], []
    for upload in files:
        name = upload.filename or "document"
        data = await upload.read()
        if len(data) > MAX_UPLOAD_BYTES:
            errors.append(f"{name}: larger than 15 MB.")
            continue
        suffix = Path(name).suffix.lower()
        try:
            if suffix in IMAGE_MIME_TYPES:
                if not llm.ready:
                    raise UnsupportedDocument(f"{name}: reading photos needs an AI model. Add an API key to .env first.")
                text = await llm.transcribe_image(data, IMAGE_MIME_TYPES[suffix])
            else:
                text = extract_text(name, data)
        except UnsupportedDocument as exc:
            errors.append(str(exc))
            continue
        except openai.APIError as exc:
            errors.append(f"{name}: {describe_llm_error(exc)}")
            continue
        added.append(case.add_document(name, text).id)
    return {"case": case.public_state(), "added": added, "errors": errors}


@app.patch("/api/cases/{case_id}/documents/{doc_id}")
def update_document(case_id: str, doc_id: str, body: DocTypeUpdate, request: Request) -> dict[str, Any]:
    case = _get_case(request, case_id)
    if doc_id not in case.documents:
        raise HTTPException(404, "Document not found.")
    if body.doc_type not in DOC_TYPES:
        raise HTTPException(400, f"doc_type must be one of: {', '.join(DOC_TYPES)}")
    case.documents[doc_id].doc_type = body.doc_type
    return case.public_state()


@app.delete("/api/cases/{case_id}/documents/{doc_id}")
def delete_document(case_id: str, doc_id: str, request: Request) -> dict[str, Any]:
    case = _get_case(request, case_id)
    if case.documents.pop(doc_id, None) is None:
        raise HTTPException(404, "Document not found.")
    return case.public_state()


@app.post("/api/cases/{case_id}/sample")
def load_sample(case_id: str, request: Request) -> dict[str, Any]:
    case = _get_case(request, case_id)
    existing = {doc.filename for doc in case.documents.values()}
    for path in sorted(SAMPLES_DIR.glob("*.txt")):
        if path.name not in existing:
            case.add_document(path.name, path.read_text(encoding="utf-8"))
    return case.public_state()


@app.post("/api/cases/{case_id}/run")
async def run(case_id: str, body: RunRequest, request: Request) -> StreamingResponse:
    case = _get_case(request, case_id)
    llm = request.app.state.llm
    if not llm.ready:
        raise HTTPException(400, "No AI model configured. Copy .env.example to .env, add a free API key and restart.")
    if case.busy:
        raise HTTPException(409, "The agent is already working on this case.")
    if body.mode:
        if not case.documents:
            raise HTTPException(400, "Upload your documents or load the sample case first.")
        try:
            message = kickoff_message(body.mode, body.message)
        except ValueError as exc:
            raise HTTPException(400, str(exc)) from exc
        case.reset_analysis()
    else:
        message = body.message.strip()
        if not message:
            raise HTTPException(400, "Message is empty.")

    case.busy = True
    max_steps = request.app.state.max_agent_steps

    async def stream():
        try:
            async for event in run_agent(case, message, llm, max_steps=max_steps):
                yield _sse(event)
        except Exception as exc:  # show provider failures in the activity feed instead of dropping the stream
            logger.exception("Agent run failed")
            yield _sse({"type": "error", "message": describe_llm_error(exc), "case": case.public_state()})
        finally:
            case.busy = False

    return StreamingResponse(stream(), media_type="text/event-stream", headers={"Cache-Control": "no-cache"})


app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
