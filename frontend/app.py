"""
Streamlit chat frontend for the Study Assistant RAG project.

Run with:
    cd frontend
    streamlit run app.py
"""

import streamlit as st

from api_client import API_BASE_URL, BackendError, ask_question, check_health

st.set_page_config(page_title="Study Assistant", page_icon="📚", layout="centered")

st.title("📚 Study Assistant")
st.caption(
    "Ask a question about the study documents. Answers are grounded in the "
    "retrieved sources -- if the documents don't contain the answer, the "
    "assistant will say so instead of guessing."
)

with st.sidebar:
    st.subheader("Backend status")
    st.write(f"API URL: `{API_BASE_URL}`")
    if check_health():
        st.success("Backend is reachable ✅")
    else:
        st.error("Backend is NOT reachable ❌")
        st.caption("Start it with: `uvicorn app.main:app --reload` inside backend/")

# Keep the chat history in Streamlit's session state so it survives reruns
# within the same browser session (it resets on page refresh, which is fine
# for a demo -- we're not persisting a database of past chats).
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render the existing conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            with st.expander("Sources used for this answer"):
                for src in message["sources"]:
                    st.markdown(f"**{src['source']}** (chunk `{src['chunk_id']}`)")
                    st.caption(src["snippet"])

# Chat input box
question = st.chat_input("Ask a question about your documents...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("_Thinking..._")  # loading state
        try:
            result = ask_question(question)
            answer = result.get("answer", "")
            sources = result.get("sources", [])

            placeholder.markdown(answer)
            if sources:
                with st.expander("Sources used for this answer"):
                    for src in sources:
                        st.markdown(f"**{src['source']}** (chunk `{src['chunk_id']}`)")
                        st.caption(src["snippet"])

            st.session_state.messages.append(
                {"role": "assistant", "content": answer, "sources": sources}
            )
        except BackendError as err:
            friendly_message = f"⚠️ {err}"
            placeholder.markdown(friendly_message)
            st.session_state.messages.append({"role": "assistant", "content": friendly_message})
