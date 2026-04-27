<p align="center">
  <img src="https://img.icons8.com/fluency/96/shopping-cart.png" alt="ShoppingWithAI Logo" width="80" />
</p>

<h1 align="center">ShoppingWithAI</h1>

<p align="center">
  <a href="#english">English</a> | <a href="#chinese">中文</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Model-Qwen--3.5--Plus-purple.svg?style=flat-square" />
  <img src="https://img.shields.io/badge/Framework-LangGraph-orange.svg?style=flat-square" />
  <img src="https://img.shields.io/badge/UI-Streamlit-ff4b4b.svg?style=flat-square" />
  <img src="https://img.shields.io/badge/VectorDB-FAISS-green.svg?style=flat-square" />
</p>

---

<h2 id="english" align="center">🇬🇧 English</h2>

<h2 align="center">Intelligent Shopping Decision Engine</h2>

<p align="center">
  <strong>A multi-agent collaborative AI shopping assistant powered by LangGraph</strong>
</p>

## 🎯 Scope

**ShoppingWithAI** is more than a chatbot — it's a closed-loop decision system that **understands needs, retrieves knowledge, and compares prices**. By decomposing complex shopping logic into LangGraph nodes, it guides users through the entire journey from "just browsing" to "placing the perfect order", like a top-tier sales consultant.

- [x] **Intelligent Semantic Routing**: Automatically identifies intent (price inquiry, comparison, expert consultation, or casual chat)
- [x] **Deep RAG Retrieval**: FAISS-based long-term memory with a professional product knowledge base
- [x] **Multi-turn Conversation Context**: Accurately remembers previous recommendations and supports follow-up queries
- [x] **Visual Shopping Interface**: Immersive interaction experience built with Streamlit
- [x] **Automated Device Comparison**: Semantic matching across the device library via Embedding technology

---

## 🧠 Architecture

The project uses a **LangGraph**-driven multi-agent workflow, making every decision node transparent and traceable:

1. **Router Agent**: Intent recognition — routes traffic to RAG, price lookup, or general answering.
2. **RAG Node**: Local `docs.txt` vector search for professional product specs and buying guides.
3. **Pricing Node**: Simulated real-time price query engine with reproducible demo prices.
4. **Recommender Node**: Semantic matching in the device library based on user budget, profile, and scenario.

---

## 🚀 Quick Start

### 1. Set Up Environment
```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
python -m pip install -r requirements.txt
# Editable install to ensure correct module imports
python -m pip install -e .
```

### 3. Configure API Key

Create a `.env` file in the project root:
```env
DASHSCOPE_API_KEY=your_dashscope_api_key
```

### 4. Run the App

- **CLI mode**:
```bash
python scripts/run_cli.py
```

- **Streamlit GUI**:
```bash
python -m streamlit run app_streamlit.py
```

---

## 📅 Roadmap

- [x] **v0.1**: Core logic up and running — routing and direct answers.
- [x] **v0.5**: FAISS vector search integrated with a phone-shopping knowledge base.
- [x] **v0.8**: Multi-turn conversation support and recommendation algorithm improvements.
- [x] **v1.0**: Streamlit UI launched with full visual interaction redesign.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | Qwen3.5-Plus via DashScope |
| Orchestration | [LangGraph](https://github.com/langchain-ai/langgraph) |
| Vector Database | FAISS |
| Frontend | Streamlit |
| Data Processing | LangChain, RapidFuzz |

---

## 📝 Notes

- **Price data**: Currently mock-implemented to ensure reproducible results in demo environments.
- **Cache**: Vector index cache files are generated automatically — no manual setup required.

---

<p align="center">
<i>"Know what you need, love what you get — your AI navigator for the shopping age."</i>
</p>

---
---

<h2 id="chinese" align="center">🇨🇳 中文</h2>

<h2 align="center">智能导购决策引擎</h2>

<p align="center">
  <strong>基于 LangGraph 的多智能体协作式 AI 购物助手</strong>
</p>

## 🎯 项目愿景

**ShoppingWithAI** 不仅仅是一个聊天机器人，它是一个能够**理解需求、检索知识、比对价格**的闭环决策系统。通过将复杂的导购逻辑拆解为 LangGraph 节点，它能像金牌导购一样引导用户完成从"随便看看"到"精准下单"的全过程。

- [x] **智能语义路由**：自动识别意图（问价、比价、专业知识咨询或闲聊）
- [x] **深度 RAG 检索**：基于 FAISS 的长时记忆与专业文档库检索
- [x] **多轮对话上下文**：精准记住"上一次推荐"，支持连续追问
- [x] **可视化导购界面**：基于 Streamlit 的沉浸式交互体验
- [x] **自动化设备比选**：通过 Embedding 技术在设备库中实现精准推荐

---

## 🧠 核心架构

项目采用 **LangGraph** 驱动的多 Agent 工作流，确保每一个决策节点都清晰可见：

1. **Router Agent**: 意图识别，决定流量分发至 RAG、价格查询或通用回答。
2. **RAG Node**: 本地 `docs.txt` 向量检索，处理专业产品参数和选购知识。
3. **Pricing Node**: 模拟实时价格查询引擎，输出具备一致性的演示价格。
4. **Recommender Node**: 基于用户预算、人群及场景，在设备库中进行语义匹配。

---

## 🚀 快速开始

### 1. 环境准备
```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 2. 安装依赖
```bash
python -m pip install -r requirements.txt
# 执行可编辑安装以确保模块导入正常
python -m pip install -e .
```

### 3. 配置密钥

在项目根目录创建 `.env` 文件：
```env
DASHSCOPE_API_KEY=你的阿里灵积API密钥
```

### 4. 启动程序

- **命令行体验 (CLI)**:
```bash
python scripts/run_cli.py
```

- **图形化界面 (Streamlit)**:
```bash
python -m streamlit run app_streamlit.py
```

---

## 📅 演进历程

- [x] **v0.1**: 基础逻辑跑通，实现路由与直答。
- [x] **v0.5**: 引入 FAISS 向量检索，支持手机导购专业知识库。
- [x] **v0.8**: 增加多轮对话支持与设备推荐算法优化。
- [x] **v1.0**: Streamlit UI 发布，完成可视化交互重构。

---

## 🛠️ 技术栈

| 层级 | 技术 |
|---|---|
| 大语言模型 | 通义千问 Qwen3.5-Plus (DashScope) |
| 编排框架 | [LangGraph](https://github.com/langchain-ai/langgraph) |
| 向量数据库 | FAISS |
| 前端界面 | Streamlit |
| 数据处理 | LangChain, RapidFuzz |

---

## 📝 开发备注

- **价格数据**: 目前为 Mock 实现，确保演示环境下结果的可重复性。
- **缓存说明**: 向量索引缓存文件会自动生成，无需手动配置。

---

<p align="center">
<i>"懂你所需，荐你所爱 —— AI 时代的购物领航员。"</i>
</p>
