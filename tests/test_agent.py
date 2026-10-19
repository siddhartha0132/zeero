import asyncio
import json

from fastapi.testclient import TestClient

from app.agent import run_agent
from app.llm import AssistantTurn, ToolCall
from app.main import app
from app.store import Case


class ScriptedLLM:
    """Stands in for the model: returns pre-written turns and records what it was sent."""

    ready = True
    model_name = "scripted"

    def __init__(self, turns):
        self._turns = list(turns)
        self.seen_messages = []

    async def complete(self, messages, tools):
        self.seen_messages.append(list(messages))
        return self._turns.pop(0)

    async def transcribe_image(self, data, mime_type):
        return "transcribed"


def tool_turn(*calls):
    tool_calls = [ToolCall(id=f"call_{i}", name=name, arguments=json.dumps(args)) for i, (name, args) in enumerate(calls)]
    raw = {
        "role": "assistant",
        "tool_calls": [
            {"id": c.id, "type": "function", "function": {"name": c.name, "arguments": c.arguments}} for c in tool_calls
        ],
    }
    return AssistantTurn(content="", tool_calls=tool_calls, raw=raw)


def text_turn(text):
    return AssistantTurn(content=text, tool_calls=[], raw={"role": "assistant", "content": text})


def script():
    return [
        tool_turn(
            ("update_plan", {"steps": [{"title": "Read documents", "status": "in_progress"}]}),
            ("list_documents", {}),
        ),
        tool_turn(("record_verdict", {"outcome": "rejection_contestable", "headline": "Moratorium applies",
                                      "confidence": "high", "key_findings": [], "next_steps": []})),
        text_turn("Your rejection can be challenged."),
    ]


def collect(case, llm, message="hi"):
    async def gather():
        return [event async for event in run_agent(case, message, llm)]

    return asyncio.run(gather())


def test_agent_loop_runs_tools_and_feeds_results_back():
    case = Case(id="c1")
    case.add_document("policy.txt", "POLICY WORDING\nSum insured Rs. 5,00,000")
    llm = ScriptedLLM(script())

    events = collect(case, llm)

    types = [event["type"] for event in events]
    assert types.count("tool_call") == 3
    assert types[-1] == "done"
    assert case.plan[0]["title"] == "Read documents"
    assert case.verdict["outcome"] == "rejection_contestable"
    # the second model call must see both tool results, answered by id
    second_call = llm.seen_messages[1]
    assert [m["tool_call_id"] for m in second_call if m["role"] == "tool"] == ["call_0", "call_1"]
    assert "policy.txt" in second_call[-1]["content"]


def test_follow_up_keeps_conversation():
    case = Case(id="c2")
    collect(case, ScriptedLLM(script()))
    llm = ScriptedLLM([text_turn("Sure, here it is in Hindi.")])

    collect(case, llm, "explain in Hindi")

    sent = llm.seen_messages[0]
    assert sent[0]["role"] == "system"
    assert sent[-1] == {"role": "user", "content": "explain in Hindi"}
    assert any(m.get("content") == "Your rejection can be challenged." for m in sent)


def test_api_end_to_end_with_sample_case():
    app.state.llm = ScriptedLLM(script())
    client = TestClient(app)

    case_id = client.post("/api/cases").json()["id"]
    state = client.post(f"/api/cases/{case_id}/sample").json()
    assert len(state["documents"]) == 4

    response = client.post(f"/api/cases/{case_id}/run", json={"mode": "appeal", "message": "Please help"})
    assert response.status_code == 200
    events = [json.loads(line[6:]) for line in response.text.splitlines() if line.startswith("data: ")]
    assert events[-1]["type"] == "done"
    assert events[-1]["case"]["verdict"]["headline"] == "Moratorium applies"
    assert client.get(f"/api/cases/{case_id}").json()["busy"] is False


def test_api_rejects_run_without_documents_and_bad_uploads():
    app.state.llm = ScriptedLLM([])
    client = TestClient(app)
    case_id = client.post("/api/cases").json()["id"]

    assert client.post(f"/api/cases/{case_id}/run", json={"mode": "appeal"}).status_code == 400

    upload = client.post(f"/api/cases/{case_id}/documents", files=[("files", ("virus.exe", b"MZ", "application/octet-stream"))])
    assert upload.json()["added"] == []
    assert "unsupported" in upload.json()["errors"][0]
