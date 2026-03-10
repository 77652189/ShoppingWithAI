# ShoppingWithAI
AI导购（Shopping Assistant）项目：用户输入 → LangGraph(agent) → (RAG/价格查询/直接回答) → 输出。

## Features (MVP)
- 路由：根据用户问题简单判断走 RAG /价格查询 /直接回答
- RAG：本地 `data/docs.txt` + FAISS（可用则用）
-价格查询：暂时 stub，后续接真实价格API
-直接回答：Qwen `qwen3.5-plus`（DashScope OpenAI兼容接口）

## Setup
- 在根目录准备 `.env`：

```env
DASHSCOPE_API_KEY=你的key
```

## Run

```bash
# (推荐) 在项目根目录
python -m pip install -e .
python scripts/run_cli.py
```

## Notes
-目前 `price_lookup` 支持 Serper（Google Shopping）可选集成：设置 `SERPER_API_KEY` 后会尝试返回一个 best-effort 的价格/链接；不设置则退化为 stub。

