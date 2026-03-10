from __future__ import annotations

from .config import load_settings
from .graph import build_graph


def run_once(user_input: str) -> str:
	settings = load_settings()
	graph = build_graph(settings)
	out = graph.invoke({"user_input": user_input})
	return out.get("answer", "")


def main() -> None:
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
			print(run_once(q))
		except Exception as e:
			print(f"运行失败：{e}")
			print("提示：请在项目根目录 .env里设置 DASHSCOPE_API_KEY=...")


if __name__ == "__main__":
	main()
