from __future__ import annotations

from typing import Literal, TypedDict


ToolName = Literal["rag", "price_lookup", "direct_answer"]


class FinalAnswer(TypedDict):
 answer: str
 tool_used: ToolName
