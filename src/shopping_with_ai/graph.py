from __future__ import annotations

import os
import time
import threading
from typing import Any, Dict, List, Literal, TypedDict

from langgraph.graph import END, StateGraph

from .config import Settings
from .llm import make_client
from .price import lookup_price
from .rag import rag_search
from .devices import recommend_devices
from .types import Message


class State(TypedDict, total=False):
	user_input: str
	history: List[Message]
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
			"哪款",
			"哪个",
			"预算",
			"帮我",
			"好用",
			"值得",
			"推荐下",
			"选",
		]
	):
		return "rag"

	return "direct_answer"


def _do_rag(state: State) -> State:
	hits = rag_search(state["user_input"])
	state["rag_hits"] = [hit.__dict__ for hit in hits]

	# Optional debug: show routing + raw hits.
	if os.getenv("DEBUG_RAG", "0") == "1":
		print("\n\n[DEBUG] route=rag")
		if not hits:
			print("[DEBUG] hits=0")
		else:
			for h in state["rag_hits"]:
				print(f"[DEBUG] doc#{h.get('doc_id')} score={h.get('score'):.3f} :: {h.get('text')}")
	return state


def _do_price(state: State) -> State:
	quote = lookup_price(state["user_input"])
	state["price"] = quote.__dict__
	return state


def _direct_answer(state: State, settings: Settings, stream: bool) -> State:
	client = make_client(settings)

	# Compose a visible citation block so you can verify RAG is being used.
	# Use an ASCII header too, in case the terminal encoding garbles Chinese.
	hits = state.get("rag_hits") or []
	if hits:
		lines = []
		for h in hits:
			text = (h.get("text") or "").strip().replace("\n", " ")
			if len(text) >160:
				text = text[:160] + "…"
			lines.append(f"- doc#{h.get('doc_id')} score={h.get('score'):.3f}: {text}")
			if len(lines) >=5:
				break
		citations = "\n\n[RAG_CITATIONS]\n" + "\n".join(lines)
	else:
		citations = "\n\n[RAG_CITATIONS]\n(none)"

	# "DeepSeek-style" visible reasoning without exposing chain-of-thought:
	# We provide a short, user-facing rationale bullets (not hidden reasoning tokens).
	rationale = "\n\n[RATIONALE]\n"
	rationale += "- Confirm scenario/persona (who uses it, for what, where)\n"
	rationale += "- Translate needs -> specs (screen/battery/speaker/signal/durability/usability)\n"
	rationale += "- Give actionable plan (budget tiers/setup steps/pitfalls)\n"

	sys = (
		"You are an AI shopping assistant. Answer in Chinese. "
		"Be concrete and actionable. "
		"Use the provided RAG snippets when relevant and do not invent citations. "
		"Do not reveal private chain-of-thought. Provide brief rationale bullets only. "
		"If you don't know exact prices, say so and suggest how to check."
	)

	context_parts: List[str] = []
	if hits:
		context_parts.append("RAG检索结果：\n" + "\n".join([h["text"] for h in hits]))
	if state.get("price"):
		context_parts.append(f"价格查询结果：{state['price']}")

	# add device recommendations (mock database)
	devices = recommend_devices(state["user_input"], k=3)
	device_block = ""
	if devices:
		lines = []
		for d in devices:
			lines.append(f"- {d.name} | {d.price_range} | 亮点: {', '.join(d.features[:3])}")
		device_block = "\n\n[DEVICE_RECS]\n" + "\n".join(lines)
		context_parts.append("机型推荐（模拟库）：\n" + "\n".join(lines))

	context = "\n\n".join(context_parts)

	# include short conversation context
	history = state.get("history") or []
	# Keep last few turns to avoid prompt bloat
	trimmed = history[-6:]
	messages: List[Dict[str, str]] = [{"role": "system", "content": sys}]
	for m in trimmed:
		messages.append({"role": m["role"], "content": m["content"]})

	user = state["user_input"] if not context else f"{state['user_input']}\n\n{context}"
	messages.append({"role": "user", "content": user})

	if stream:
		resp = client.chat.completions.create(
			model=settings.model,
			messages=messages,
			stream=True,
		)
		chunks: List[str] = []

		# --- pseudo progress bar (0-90%) while waiting for first token ---
		progress_stop = threading.Event()
		progress_started = threading.Event()

		def _progress_bar():
			pct =0
			while not progress_stop.is_set():
				# slowly advance to90%
				pct = min(90, pct +1)
				bar_len =20
				filled = int(bar_len * pct /100)
				bar = "=" * filled + "." * (bar_len - filled)
				print(f"\r[Generating] {pct:02d}% [{bar}]", end="", flush=True)
				progress_started.set()
				time.sleep(0.2)
			# clear line when stopping
			print("\r" + " " *40 + "\r", end="", flush=True)

		thread = threading.Thread(target=_progress_bar, daemon=True)
		thread.start()

		# Some terminals buffer stdout and make streaming look "not streaming".
		# We print token chunks and optionally add a tiny delay so it's visibly incremental.
		stream_delay_ms = int(os.getenv("STREAM_DELAY_MS", "0"))
		first_token = True
		for chunk in resp:
			delta = chunk.choices[0].delta
			content = getattr(delta, "content", None)
			if content:
				if first_token:
					# stop progress and start real output
					progress_stop.set()
					first_token = False
				print(content, end="", flush=True)
				chunks.append(content)
				if stream_delay_ms >0:
					time.sleep(stream_delay_ms /1000.0)

		# ensure progress thread stops even if no tokens
		progress_stop.set()
		answer_text = "".join(chunks)
	else:
		resp = client.chat.completions.create(model=settings.model, messages=messages)
		answer_text = resp.choices[0].message.content or ""

	# Insert citations before a common closing phrase so it shows up in the main body.
	closing_markers = ["祝您购物愉快", "祝您购物愉快！", "祝您购物愉快!", "购物愉快"]
	inserted = False
	for marker in closing_markers:
		idx = answer_text.rfind(marker)
		if idx != -1:
			answer_text = answer_text[:idx].rstrip() + citations + "\n\n" + answer_text[idx:]
			inserted = True
			break
	if not inserted:
		answer_text = answer_text.rstrip() + citations

	# IMPORTANT: when stream=True, the main answer was already printed token-by-token above.
	# So we must print the citations block here as well, otherwise the user will not see it.
	if stream:
		print(citations, end="", flush=True)

	# If we have device recs, surface them in the visible answer too (not only hidden context).
	if devices:
		rec_lines = [
			f"- {d.name}（{d.price_range}）: {', '.join(d.features[:3])}"
			for d in devices
		]
		rec_text = "\n\n【机型推荐（模拟库）】\n" + "\n".join(rec_lines)
		answer_text = answer_text.rstrip() + rec_text
		# Also attach as an ASCII block for easy inspection
		answer_text = answer_text + device_block

	state["answer"] = answer_text + rationale
	# Keep rationale printed after the main body.
	print(rationale, end="", flush=True)
	return state


def build_graph(settings: Settings, stream: bool = False):
	g = StateGraph(State)
	g.add_node("route", lambda s: {**s, "route": _route(s)})
	g.add_node("rag", _do_rag)
	g.add_node("price_lookup", _do_price)
	g.add_node("direct_answer", lambda s: _direct_answer(s, settings, stream=stream))

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
