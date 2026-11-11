import re
import streamlit as st
from rag_chain import answer

st.set_page_config(
    page_title="Zahra — Digital AI Clone", 
    page_icon="🌊", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Coastal Ocean Palette & Minimalist Typography
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    html, body, p, h1, h2, h3, h4, h5, h6, span, label, input, textarea, button {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Floating Hero Header (Centered, Minimal, Compact) */
    .hero-container {
        max-width: 640px;
        margin: 0 auto 24px auto;
        text-align: center;
        padding: 24px 28px;
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #0f766e 100%);
        border-radius: 20px;
        box-shadow: 0 12px 32px -8px rgba(15, 23, 42, 0.28);
        border: 1px solid rgba(56, 189, 248, 0.25);
    }

    .hero-title {
        font-size: 2.1rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        background: linear-gradient(135deg, #ffffff 40%, #7dd3fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }

    .hero-subtitle {
        font-size: 0.95rem;
        font-weight: 500;
        color: #cbd5e1;
        letter-spacing: 0.2px;
        margin: 0;
    }

    .hero-pill {
        display: inline-block;
        margin-top: 10px;
        padding: 4px 14px;
        background: rgba(14, 165, 233, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.35);
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.4px;
    }

    /* Sidebar Styling & Fill Expansion */
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }

    .sidebar-section-title {
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #0284c7;
        margin-bottom: 8px;
    }

    .sidebar-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #0284c7;
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
    }

    .sidebar-card h4 {
        color: #0f172a;
        font-size: 1rem;
        font-weight: 700;
        margin: 0 0 8px 0;
    }

    .sidebar-card p {
        color: #475569;
        font-size: 0.88rem;
        line-height: 1.55;
        margin-bottom: 8px;
    }

    .sidebar-list {
        margin: 0;
        padding-left: 18px;
        color: #475569;
        font-size: 0.85rem;
        line-height: 1.6;
    }

    /* Sample Question Pill Buttons */
    div.stButton > button[kind="secondary"] {
        background: #ffffff !important;
        color: #0284c7 !important;
        border: 1.5px solid #0284c7 !important;
        border-radius: 20px !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        padding: 8px 16px !important;
        box-shadow: 0 2px 6px rgba(2, 132, 199, 0.08) !important;
        transition: all 0.2s ease-in-out !important;
    }

    div.stButton > button[kind="secondary"]:hover {
        background: #f0f9ff !important;
        border-color: #0369a1 !important;
        color: #0369a1 !important;
        transform: translateY(-1px);
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Controls & Expanded Knowledge Profile
with st.sidebar:
    st.markdown("<p class='sidebar-section-title'>⚡ Retrieval Engine</p>", unsafe_allow_html=True)
    mode = st.radio(
        "Search Mode", 
        ["BM25 Lexical", "Dense Vector", "Hybrid (RRF)"], 
        index=2,
        help="Hybrid merges lexical BM25 search with dense vector embeddings via Reciprocal Rank Fusion (RRF)."
    )

    st.markdown("---")
    
    st.markdown("<p class='sidebar-section-title'>🌊 Digital Identity Profile</p>", unsafe_allow_html=True)
    st.markdown("""
        <div class="sidebar-card">
            <h4>Zahra Mumtaz</h4>
            <p>Interactive Retrieval-Augmented Generation (RAG) agent trained on Zahra's verified personal documents, research repositories, and technical stack.</p>
            <ul class="sidebar-list">
                <li><b>Academic Research:</b> Multimodal emotion analysis (Emora) & Guarded AI waste vision (TrashSense).</li>
                <li><b>Engineering Stack:</b> Python, PyTorch, LangGraph, OpenCV, FastAPI, and Groq SDK.</li>
                <li><b>Personal Insights:</b> Study methodologies, hackathon projects, and culinary baking recipes.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="sidebar-card" style="border-left-color: #0d9488;">
            <h4>⚙️ Architecture Specs</h4>
            <p style="font-size: 0.83rem; margin: 0;">
                • <b>LLM Backbone:</b> Groq Qwen-2.5 32B<br>
                • <b>Vector Search:</b> Sentence-Transformers<br>
                • <b>Fusion Algorithm:</b> Reciprocal Rank
            </p>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Minimalist Centered Hero Header
st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Zahra Mumtaz</div>
        <div class="hero-subtitle">Digital AI Clone</div>
        <div class="hero-pill">Hybrid RAG &bull; Groq Inference Engine</div>
    </div>
""", unsafe_allow_html=True)

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "Hello! I am Zahra's AI Digital Clone. Feel free to ask about my final year research project **Emora**, technical software stack, study workflows, or signature baking recipes!",
            "hits": []
        }
    ]

def clean_text_snippet(raw_text):
    return re.sub(r'^#+\s*', '', raw_text.strip())

# Render Chat Feed with Custom Avatars
for msg in st.session_state.messages:
    avatar_icon = "🌊" if msg["role"] == "assistant" else "✨"
    with st.chat_message(msg["role"], avatar=avatar_icon):
        st.markdown(msg["content"])
        
        if msg.get("hits"):
            with st.expander("🔍 View Hybrid RAG Evidence & Context Chunks", expanded=False):
                for idx, (chunk, score) in enumerate(msg["hits"], 1):
                    source_file = chunk.get("source", "Unknown")
                    chunk_id = chunk.get("chunk_id", "N/A")
                    score_fmt = f"{score:.4f}"
                    snippet = clean_text_snippet(chunk.get("text", ""))
                    
                    st.markdown(f"**Match #{idx}** | `Source: {source_file}` | `Chunk: #{chunk_id}` | `RRF Score: {score_fmt}`")
                    st.code(snippet, language=None, wrap_lines=True)

# Suggested Prompt Cards
prompt_to_process = None
if len(st.session_state.messages) <= 1:
    st.markdown("<p style='font-weight:600; color:#0f2b3c; text-align: center; margin-bottom: 12px;'>Suggested Questions:</p>", unsafe_allow_html=True)
    _, center_col, _ = st.columns([0.1, 0.8, 0.1])
    with center_col:
        col1, col2, col3 = st.columns(3)
        if col1.button("Tell me about Emora", type="secondary", use_container_width=True):
            prompt_to_process = "Tell me about your final year project Emora."
        if col2.button("What tools do you use?", type="secondary", use_container_width=True):
            prompt_to_process = "What programming languages and framework tools do you use daily?"
        if col3.button("Signature baking dish?", type="secondary", use_container_width=True):
            prompt_to_process = "What is your signature culinary dish or dessert to bake?"

# Fixed Bottom Input Bar
user_input = st.chat_input("Ask Zahra anything...")
if user_input:
    prompt_to_process = user_input

# Query Execution Logic
if prompt_to_process:
    # Normalize mode string for backend chain
    backend_mode = "Hybrid"
    if "BM25" in mode:
        backend_mode = "BM25 only"
    elif "Dense" in mode:
        backend_mode = "Dense only"

    st.session_state.messages.append({"role": "user", "content": prompt_to_process, "hits": []})
    with st.chat_message("user", avatar="✨"):
        st.markdown(prompt_to_process)

    with st.chat_message("assistant", avatar="🌊"):
        with st.spinner("Searching knowledge base..."):
            reply, hits = answer(prompt_to_process, backend_mode)
            st.markdown(reply)

            if hits:
                with st.expander("🔍 View Hybrid RAG Evidence & Context Chunks", expanded=False):
                    for idx, (chunk, score) in enumerate(hits, 1):
                        source_file = chunk.get("source", "Unknown")
                        chunk_id = chunk.get("chunk_id", "N/A")
                        score_fmt = f"{score:.4f}"
                        snippet = clean_text_snippet(chunk.get("text", ""))
                        
                        st.markdown(f"**Match #{idx}** | `Source: {source_file}` | `Chunk: #{chunk_id}` | `RRF Score: {score_fmt}`")
                        st.code(snippet, language=None, wrap_lines=True)

            st.session_state.messages.append({"role": "assistant", "content": reply, "hits": hits})
            st.rerun()