from __future__ import annotations

from dataclasses import dataclass
import os

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
	dashscope_api_key: str
	dashscope_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
	model: str = "qwen3.5-plus"
	embedding_model: str = "text-embedding-v3"


def load_settings() -> Settings:
	"""Load settings from .env / environment.

	Expects DASHSCOPE_API_KEY in env.
	"""
	load_dotenv(override=False)
	key = os.getenv("DASHSCOPE_API_KEY")
	if not key:
		raise RuntimeError(
			"Missing DASHSCOPE_API_KEY in environment (set it in .env or system env)."
		)
	return Settings(dashscope_api_key=key)
