import streamlit as st
from rag_chain import answer

st.set_page_config(page_title="Zahra Mumtaz — Digital AI Clone", page_icon="🌊", layout="wide")

st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 24px;
        background: linear-gradient(135deg, #0f2b3c 0%, #1a4b6e 100%);
        color: white;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    </style>
    <div class="main-header">
        <h1>Zahra Mumtaz</h1>
        <p>Senior Software Engineering Student &bull; AI Enthusiast</p>
    </div>
""", unsafe_allow_html=True)

st.info("Interactive RAG AI Clone — Ask about my academic research (Emora, TrashSense), technical stack, study methodology, or culinary baking!")

col1, col2 = st.columns([3, 1])

with col1:
    question = st.text_input("Your Question", placeholder="e.g., Tell me about your final year project Emora...")

with col2:
    mode = st.radio("Retrieval Mode", ["BM25 only", "Dense only", "Hybrid"], index=2)

if st.button("Ask Zahra", type="primary"):
    if not question.strip():
        st.warning("Please enter a question!")
    else:
        with st.spinner("Thinking..."):
            reply, hits = answer(question, mode)
            st.markdown("### Zahra's Answer")
            st.write(reply)
            
            st.markdown("### Hybrid RAG Evidence & Context Chunks")
            rows = [{"Source File": c["source"], "Chunk ID": c["chunk_id"], "Score": round(score, 4), "Matched Snippet": c["text"][:250] + "..."} for c, score in hits]
            st.dataframe(rows, use_container_width=True)