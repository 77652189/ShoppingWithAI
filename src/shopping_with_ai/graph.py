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

	MVP rule: default most shopping-intent queries to RAG so we can cite docs.
	Later: replace with LLM router (function calling) or a classifier.
	"""
	q = state["user_input"].lower()

	# price intent
	if any(x in q for x in ["price", "价格", "$", "usd", "多少钱", "报价", "价位"]):
		return "price_lookup"

	# shopping / recommendation intent (Chinese + English)
	if any(
		x in q
		for x in [
			"recommend",
			"推荐",
			"compare",
			"对比",
			"哪个好",
			"测评",
			"怎么选",
			"选购",
			"买",
			"想买",
			"给",
			"送",
			"手机",
			"耳机",
			"电脑",
			"平板",
			"相机",
			"路由器",
			"电视",
		]
	):
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

	# Compose a visible citation block so you can verify RAG is being used.
	citations = ""
	hits = state.get("rag_hits") or []
	if hits:
		lines = []
		for h in hits:
			# keep each line short
			text = (h.get("text") or "").strip().replace("\n", " ")
			if len(text) >160:
				text = text[:160] + "…"
			lines.append(f"- doc#{h.get('doc_id')} score={h.get('score'):.3f}: {text}")
			if len(lines) >=5:
				break
		citations = "\n\n【参考资料 / RAG命中】\n" + "\n".join(lines)
	else:
		citations = "\n\n【参考资料 / RAG命中】(无)"

	sys = (
		"You are an AI shopping assistant. Answer in Chinese. "
		"Use the provided RAG snippets when relevant and do not invent citations. "
		"If you don't know exact prices, say so and suggest how to check."
	)

	context_parts: List[str] = []
	if hits:
		context_parts.append("RAG检索结果：\n" + "\n".join([h["text"] for h in hits]))
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
	state["answer"] = (resp.choices[0].message.content or "") + citations
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
