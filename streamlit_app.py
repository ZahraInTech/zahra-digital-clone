import re
import streamlit as st
from rag_chain import answer

st.set_page_config(
    page_title="Zahra — Digital AI Clone", 
    page_icon="🌊", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Coastal Ocean Typography & Wave UI Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    html, body, p, h1, h2, h3, h4, h5, h6, span, label, input, textarea, button {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Organic Fluid Wave Hero Banner */
    .hero-wave-box {
        position: relative;
        background: linear-gradient(135deg, #0b192c 0%, #1e3e62 45%, #0f766e 100%);
        border-radius: 20px;
        padding: 36px 24px 56px 24px;
        text-align: center;
        color: #ffffff;
        box-shadow: 0 14px 35px -10px rgba(11, 25, 44, 0.25);
        overflow: hidden;
        margin-bottom: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .hero-name {
        font-size: 2.3rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin: 0 0 4px 0;
        background: linear-gradient(135deg, #ffffff 40%, #7dd3fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 1rem;
        font-weight: 500;
        color: #94a3b8;
        letter-spacing: 0.4px;
        margin: 0;
    }

    .hero-wave-svg {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 38px;
        pointer-events: none;
    }

    /* Sidebar Styling & Compact Fit */
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
        margin-bottom: 6px;
    }

    .sidebar-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #0284c7;
        padding: 14px 16px;
        border-radius: 12px;
        margin-top: 10px;
        margin-bottom: 14px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
    }

    .sidebar-card h4 {
        color: #0f172a;
        font-size: 0.98rem;
        font-weight: 700;
        margin: 0 0 6px 0;
    }

    .sidebar-card p {
        color: #475569;
        font-size: 0.86rem;
        line-height: 1.5;
        margin-bottom: 8px;
    }

    .sidebar-list {
        margin: 0;
        padding-left: 16px;
        color: #475569;
        font-size: 0.83rem;
        line-height: 1.55;
    }

    /* Sample Question Chips */
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

# Compact Non-Scrolling Sidebar
with st.sidebar:
    st.markdown("<p class='sidebar-section-title'>⚡ Retrieval Engine</p>", unsafe_allow_html=True)
    mode = st.radio(
        "Search Mode", 
        ["BM25 Lexical", "Dense Vector", "Hybrid"], 
        index=2,
        help="Hybrid merges lexical BM25 search with dense vector embeddings."
    )

    st.markdown("---")
    
    st.markdown("<p class='sidebar-section-title'>🌊 Digital Profile</p>", unsafe_allow_html=True)
    st.markdown("""
        <div class="sidebar-card">
            <h4>Zahra Mumtaz</h4>
            <p>Interactive AI clone trained on Zahra's personal documents, research repositories, and technical stack.</p>
            <ul class="sidebar-list">
                <li><b>Research:</b> Emora & TrashSense</li>
                <li><b>Stack:</b> Python, PyTorch, LangGraph, OpenCV, FastAPI</li>
                <li><b>Insights:</b> Workflows & Culinary baking</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Organic Wave Hero Header
st.markdown("""
    <div class="hero-wave-box">
        <h1 class="hero-name">Zahra Mumtaz</h1>
        <p class="hero-subtitle">Digital AI Clone</p>
        <svg class="hero-wave-svg" viewBox="0 0 1200 120" preserveAspectRatio="none">
            <path d="M0,0 C150,90 350,-40 500,50 C650,140 900,10 1200,40 L1200,120 L0,120 Z" fill="#ffffff" opacity="0.12"></path>
            <path d="M0,30 C200,100 450,10 700,70 C950,130 1100,20 1200,50 L1200,120 L0,120 Z" fill="#ffffff" opacity="0.2"></path>
        </svg>
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

# Render Chat Feed
for msg in st.session_state.messages:
    avatar_icon = "🌊" if msg["role"] == "assistant" else "✨"
    with st.chat_message(msg["role"], avatar=avatar_icon):
        st.markdown(msg["content"])
        
        if msg.get("hits"):
            with st.expander("🔍 View RAG Evidence & Context Chunks", expanded=False):
                for idx, (chunk, score) in enumerate(msg["hits"], 1):
                    source_file = chunk.get("source", "Unknown")
                    chunk_id = chunk.get("chunk_id", "N/A")
                    score_fmt = f"{score:.4f}"
                    snippet = clean_text_snippet(chunk.get("text", ""))
                    
                    st.markdown(f"**Match #{idx}** | `Source: {source_file}` | `Chunk: #{chunk_id}` | `Score: {score_fmt}`")
                    st.code(snippet, language=None, wrap_lines=True)

# Quick Sample Prompt Cards
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
                with st.expander("🔍 View RAG Evidence & Context Chunks", expanded=False):
                    for idx, (chunk, score) in enumerate(hits, 1):
                        source_file = chunk.get("source", "Unknown")
                        chunk_id = chunk.get("chunk_id", "N/A")
                        score_fmt = f"{score:.4f}"
                        snippet = clean_text_snippet(chunk.get("text", ""))
                        
                        st.markdown(f"**Match #{idx}** | `Source: {source_file}` | `Chunk: #{chunk_id}` | `Score: {score_fmt}`")
                        st.code(snippet, language=None, wrap_lines=True)

            st.session_state.messages.append({"role": "assistant", "content": reply, "hits": hits})
            st.rerun()