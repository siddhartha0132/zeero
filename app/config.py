from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

GEMINI_OPENAI_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"


@dataclass(frozen=True)
class Settings:
    llm_base_url: str
    llm_api_key: str
    llm_model: str
    llm_vision_model: str
    max_agent_steps: int


def load_settings() -> Settings:
    model = os.getenv("LLM_MODEL", "gemini-2.5-flash")
    return Settings(
        llm_base_url=os.getenv("LLM_BASE_URL", GEMINI_OPENAI_URL),
        llm_api_key=os.getenv("LLM_API_KEY", ""),
        llm_model=model,
        llm_vision_model=os.getenv("LLM_VISION_MODEL") or model,
        max_agent_steps=int(os.getenv("MAX_AGENT_STEPS", "30")),
    )
