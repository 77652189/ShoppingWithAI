from __future__ import annotations

from openai import OpenAI

from .config import Settings


def make_client(settings: Settings) -> OpenAI:
 return OpenAI(api_key=settings.dashscope_api_key, base_url=settings.dashscope_base_url)
