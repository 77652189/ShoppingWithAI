# ShoppingWithAI
AI导购（Shopping Assistant）项目：用户输入 → LangGraph(agent) → (RAG/价格查询/直接回答) → 输出。

## Features (MVP)
- 路由：根据用户问题简单判断走 RAG /价格查询 /直接回答
- RAG：本地 `data/docs.txt` + 向量检索（自动构建索引）
-价格查询：mock价格（可重复，用于演示）
-机型推荐：设备库 + embedding 检索
-直接回答：Qwen `qwen3.5-plus`（DashScope OpenAI兼容接口）

## Environment Setup

###1) Create venv

```bash
python -m venv .venv
# Windows:
.\.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

###2) Install dependencies

```bash
python -m pip install -r requirements.txt
# (optional) editable install for module import
python -m pip install -e .
```

###3) Configure API key

Create `.env` in project root:

```env
DASHSCOPE_API_KEY=你的key
```

## Run

```bash
# CLI
python scripts/run_cli.py
```

## Streamlit UI

```bash
python -m streamlit run app_streamlit.py
```

## Import as module

如果遇到 `ModuleNotFoundError: shopping_with_ai`，请确认已在项目根目录执行：

```bash
python -m pip install -e .
```

然后在代码里这样导入：

```python
from shopping_with_ai.app import run_once
```

## Project Timeline (from commits)

- 初始化 CLI + 基础流程跑通（路由 / RAG /直答）
- 加入 RAG 命中引用展示与可解释性输出
-价格查询改为 mock（不依赖外部 API）
- 扩展手机导购知识库（预算/人群/场景）
- 引入 embedding + FAISS 向量检索
- 扩充设备库并改用 embedding 检索推荐
-记住“上一次推荐”以支持多轮对话
- 增加 Streamlit 图形界面
- 增加 requirements.txt / README 安装说明

## Notes
-价格查询为 mock 实现（不依赖外部价格API）：基于 query生成**可重复**的演示价格。
- 向量索引缓存文件会自动生成（已在 .gitignore 中忽略）。
