"""The agent loop: the model plans, calls tools, reads the results and repeats until it has an answer."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from datetime import date
from typing import Any

from .llm import LLM
from .prompts import KICKOFF_MESSAGES, build_system_prompt
from .store import Case
from .tools import TOOL_SCHEMAS, execute_tool

MAX_TOOL_RESULT_CHARS = 12_000


def kickoff_message(mode: str, notes: str) -> str:
    if mode not in KICKOFF_MESSAGES:
        raise ValueError(f"Unknown mode {mode!r}")
    notes = notes.strip()
    return f"{KICKOFF_MESSAGES[mode]}\n\nMy notes: {notes}" if notes else KICKOFF_MESSAGES[mode]


def _parse_args(arguments: str) -> Any:
    try:
        return json.loads(arguments or "{}")
    except json.JSONDecodeError:
        return {"raw": arguments}


async def run_agent(case: Case, user_message: str, llm: LLM, max_steps: int = 30) -> AsyncIterator[dict[str, Any]]:
    """Yields UI events. The conversation is kept on the case, so follow-up messages keep full context."""
    if not case.messages:
        case.messages.append({"role": "system", "content": build_system_prompt(date.today())})
    case.messages.append({"role": "user", "content": user_message})

    for _ in range(max_steps):
        yield {"type": "status", "text": "Thinking…"}
        turn = await llm.complete(case.messages, TOOL_SCHEMAS)
        case.messages.append(turn.raw)
        if turn.content.strip():
            yield {"type": "assistant", "text": turn.content}
        if not turn.tool_calls:
            yield {"type": "done", "case": case.public_state()}
            return

        for call in turn.tool_calls:
            yield {"type": "tool_call", "id": call.id, "name": call.name, "args": _parse_args(call.arguments)}
            output = execute_tool(case, call.name, call.arguments)
            content = json.dumps(output.result, ensure_ascii=False)
            if len(content) > MAX_TOOL_RESULT_CHARS:
                content = content[:MAX_TOOL_RESULT_CHARS] + " …[truncated]"
            case.messages.append({"role": "tool", "tool_call_id": call.id, "content": content})
            yield {"type": "tool_result", "id": call.id, "name": call.name, "ok": output.ok, "summary": output.summary}
            if output.state_changed:
                yield {"type": "state", "case": case.public_state()}

    yield {
        "type": "error",
        "message": f"Stopped after {max_steps} steps. Send “continue” to let the agent keep going.",
        "case": case.public_state(),
    }
