import streamlit as st

from shopping_with_ai.app import run_once

st.set_page_config(page_title="ShoppingWithAI", page_icon="🛒")

st.title("🛒 ShoppingWithAI")
st.caption("AI 导购：RAG +价格 +机型推荐")

if "history" not in st.session_state:
 st.session_state.history = []
if "last_recs" not in st.session_state:
 st.session_state.last_recs = []
if "messages" not in st.session_state:
 st.session_state.messages = []

for msg in st.session_state.messages:
 with st.chat_message(msg["role"]):
 st.markdown(msg["content"])

user_input = st.chat_input("想买什么？")

if user_input:
 st.session_state.messages.append({"role": "user", "content": user_input})
 with st.chat_message("user"):
 st.markdown(user_input)

 with st.chat_message("assistant"):
 with st.spinner("生成中..."):
 answer = run_once(user_input, history=st.session_state.history, stream=False, last_recs=st.session_state.last_recs)
 st.markdown(answer)

 st.session_state.messages.append({"role": "assistant", "content": answer})
