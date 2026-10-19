"""Thin wrapper over any OpenAI-compatible chat API (Gemini, Groq, OpenRouter, Ollama, Claude, OpenAI)."""

from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Any, Protocol

import openai
from openai import AsyncOpenAI

from .config import Settings

TRANSCRIBE_PROMPT = (
    "Transcribe this document image into plain text exactly as written. Keep every line item, "
    "amount, date, name and table row (one row per line). Do not summarise or add commentary. "
    "Write [unclear] for anything you cannot read."
)


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: str


@dataclass
class AssistantTurn:
    content: str
    tool_calls: list[ToolCall]
    # The assistant message as the provider sent it. It goes back into the history unchanged,
    # because some providers attach data (e.g. Gemini thought signatures) that must be echoed.
    raw: dict[str, Any]


class LLM(Protocol):
    ready: bool
    model_name: str

    async def complete(self, messages: list[dict[str, Any]], tools: list[dict[str, Any]]) -> AssistantTurn: ...

    async def transcribe_image(self, data: bytes, mime_type: str) -> str: ...


class OpenAICompatibleLLM:
    def __init__(self, settings: Settings):
        self.model_name = settings.llm_model
        self._vision_model = settings.llm_vision_model
        is_local = any(host in settings.llm_base_url for host in ("localhost", "127.0.0.1"))
        self.ready = bool(settings.llm_api_key) or is_local
        self._client = AsyncOpenAI(
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key or "not-needed",
            max_retries=5,  # free tiers rate-limit hard; the SDK backs off on 429s
            timeout=180,
        )

    async def complete(self, messages: list[dict[str, Any]], tools: list[dict[str, Any]]) -> AssistantTurn:
        kwargs: dict[str, Any] = {"model": self.model_name, "messages": messages}
        if tools:
            kwargs["tools"] = tools
        response = await self._client.chat.completions.create(**kwargs)
        message = response.choices[0].message

        raw: dict[str, Any] = {"role": "assistant", **(message.model_extra or {})}
        if message.content:
            raw["content"] = message.content
        calls: list[ToolCall] = []
        if message.tool_calls:
            raw["tool_calls"] = []
            for index, call in enumerate(message.tool_calls):
                call_id = call.id or f"call_{index}"
                dumped = call.model_dump(exclude_none=True)
                dumped["id"] = call_id
                raw["tool_calls"].append(dumped)
                calls.append(ToolCall(id=call_id, name=call.function.name, arguments=call.function.arguments or "{}"))
        return AssistantTurn(content=message.content or "", tool_calls=calls, raw=raw)

    async def transcribe_image(self, data: bytes, mime_type: str) -> str:
        encoded = base64.b64encode(data).decode("ascii")
        response = await self._client.chat.completions.create(
            model=self._vision_model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": TRANSCRIBE_PROMPT},
                        {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{encoded}"}},
                    ],
                }
            ],
        )
        return response.choices[0].message.content or ""


def describe_llm_error(exc: Exception) -> str:
    """Turn provider exceptions into something a user can act on."""
    if isinstance(exc, openai.AuthenticationError):
        return "The AI provider rejected the API key. Check LLM_API_KEY in your .env file."
    if isinstance(exc, openai.RateLimitError):
        return "The AI provider's rate limit or free quota was hit. Wait a minute and retry, or switch provider in .env."
    if isinstance(exc, openai.NotFoundError):
        return f"Model not found. Check LLM_MODEL in your .env file. ({exc.message})"
    if isinstance(exc, openai.APIConnectionError):
        return "Couldn't reach the AI provider. Check your internet connection and LLM_BASE_URL."
    if isinstance(exc, openai.APIError):
        return f"AI provider error: {exc.message}"
    return f"Unexpected error: {exc}"
