from __future__ import annotations

from typing import List

from .config import load_settings
from .graph import build_graph
from .types import Message


def run_once(user_input: str, history: List[Message], stream: bool = True) -> str:
	"""Run one turn.

	- history is appended with the new user+assistant messages.
	- when stream=True, the model output is streamed to stdout.
	"""
	settings = load_settings()
	graph = build_graph(settings, stream=stream)
	out = graph.invoke({"user_input": user_input, "history": history})
	answer = out.get("answer", "")

	# update history
	history.append({"role": "user", "content": user_input})
	history.append({"role": "assistant", "content": answer})
	return answer


def main() -> None:
	history: List[Message] = []
	while True:
		try:
			q = input("\n你想买什么？(回车提交, 输入 exit退出)\n> ").strip()
		except (EOFError, KeyboardInterrupt):
			print("\nbye")
			break

		if not q:
			continue
		if q.lower() in {"exit", "quit"}:
			break

		try:
			ans = run_once(q, history=history, stream=True)
			# When stream=True, the answer is already printed; keep a newline for spacing.
			if ans.strip():
				print("\n")
		except Exception as e:
			print(f"运行失败：{e}")
			print("提示：请在项目根目录 .env里设置 DASHSCOPE_API_KEY=...")


if __name__ == "__main__":
	main()
