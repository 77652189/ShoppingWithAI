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
-目前 `price_lookup` 是 mock 实现（不依赖外部价格API）：会基于 query生成**可重复**的演示价格，用于把 agent 流程跑通。可用环境变量 `PRICE_MODE=stub`关闭。

