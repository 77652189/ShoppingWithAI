from __future__ import annotations

from typing import Any, Dict, List, Literal, TypedDict

from langgraph.graph import END, StateGraph

from .config import Settings
from .llm import make_client
from .price import lookup_price
from .rag import rag_search


class State(TypedDict, total=False):
	user_input: str
	route: Literal["rag", "price_lookup", "direct_answer"]
	rag_hits: List[Dict[str, Any]]
	price: Dict[str, Any]
	answer: str


def _route(state: State) -> str:
	"""Simple heuristic router.

	Later: replace with LLM router (function calling) or a classifier.
	"""
	q = state["user_input"].lower()
	if any(x in q for x in ["price", "价格", "$", "usd", "多少钱"]):
		return "price_lookup"
	if any(x in q for x in ["recommend", "推荐", "compare", "对比", "哪个好", "测评"]):
		return "rag"
	return "direct_answer"


def _do_rag(state: State) -> State:
	hits = rag_search(state["user_input"])
	state["rag_hits"] = [hit.__dict__ for hit in hits]
	return state


def _do_price(state: State) -> State:
	quote = lookup_price(state["user_input"])
	state["price"] = quote.__dict__
	return state


def _direct_answer(state: State, settings: Settings) -> State:
	client = make_client(settings)
	sys = (
		"You are an AI shopping assistant. Answer in Chinese. "
		"If you don't know exact prices, say so and suggest how to check."
	)
	context_parts: List[str] = []
	if state.get("rag_hits"):
		context_parts.append(
			"RAG检索结果：\n" + "\n".join([h["text"] for h in state["rag_hits"]])
		)
	if state.get("price"):
		context_parts.append(f"价格查询结果：{state['price']}")
	context = "\n\n".join(context_parts)
	user = state["user_input"] if not context else f"{state['user_input']}\n\n{context}"

	resp = client.chat.completions.create(
		model=settings.model,
		messages=[
			{"role": "system", "content": sys},
			{"role": "user", "content": user},
		],
	)
	state["answer"] = resp.choices[0].message.content or ""
	return state


def build_graph(settings: Settings):
	g = StateGraph(State)
	g.add_node("route", lambda s: {**s, "route": _route(s)})
	g.add_node("rag", _do_rag)
	g.add_node("price_lookup", _do_price)
	g.add_node("direct_answer", lambda s: _direct_answer(s, settings))

	g.set_entry_point("route")

	def _branch(state: State) -> str:
		return state.get("route", "direct_answer")

	g.add_conditional_edges(
		"route",
		_branch,
		{
			"rag": "rag",
			"price_lookup": "price_lookup",
			"direct_answer": "direct_answer",
		},
	)

	g.add_edge("rag", "direct_answer")
	g.add_edge("price_lookup", "direct_answer")
	g.add_edge("direct_answer", END)
	return g.compile()
