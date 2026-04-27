<p align="center">
  <img src="https://img.icons8.com/fluency/96/shopping-cart.png" alt="ShoppingWithAI Logo" width="80" />
</p>

<h1 align="center">ShoppingWithAI</h1>
<h2 align="center">Intelligent Shopping Decision Engine</h2>

<p align="center">
  <strong>A multi-agent collaborative AI shopping assistant powered by LangGraph</strong>
</p>

<p align="center">
  <a href="README.zh-CN.md">🇨🇳 中文</a> | 🇬🇧 English
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Model-Qwen--3.5--Plus-purple.svg?style=flat-square" />
  <img src="https://img.shields.io/badge/Framework-LangGraph-orange.svg?style=flat-square" />
  <img src="https://img.shields.io/badge/UI-Streamlit-ff4b4b.svg?style=flat-square" />
  <img src="https://img.shields.io/badge/VectorDB-FAISS-green.svg?style=flat-square" />
  <img src="https://img.shields.io/badge/Built%20with-AI%20Ensemble-blueviolet.svg?style=flat-square" />
</p>

---

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

<p align="center">
  Special thanks to the project's chief supervisors: 🐱 咪咪 & 喵喵
</p>
