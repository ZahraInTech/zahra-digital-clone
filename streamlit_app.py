import re
import streamlit as st
from rag_chain import answer

st.set_page_config(
    page_title="Zahra — Digital AI Clone", 
    page_icon="🌊", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Pastel Coastal Aesthetic + PowerPoint-Style Morph & Wave Animation CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, p, h1, h2, h3, h4, h5, h6, span, label, input, textarea, button {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Fixed Top-Right Triangular Pastel Wave Graphic */
    .top-right-wave-container {
        position: fixed;
        top: 0;
        right: 0;
        width: 340px;
        height: 340px;
        pointer-events: none;
        z-index: 99999;
        overflow: hidden;
    }

    .pastel-wave-svg {
        width: 100%;
        height: 100%;
        filter: drop-shadow(0px 10px 20px rgba(13, 148, 136, 0.15));
        animation: waveMorph 8s ease-in-out infinite alternate;
    }

    /* Keyframe Morph Effect for Geometric Side Wave */
    @keyframes waveMorph {
        0% {
            transform: translateY(0px) rotate(0deg) scale(1);
        }
        50% {
            transform: translateY(-8px) rotate(1.5deg) scale(1.02);
        }
        100% {
            transform: translateY(4px) rotate(-1deg) scale(0.99);
        }
    }

    /* Sleek Floating Header Title */
    .brand-title-wrap {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-top: 10px;
        margin-bottom: 18px;
    }

    .brand-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.6px;
        background: linear-gradient(135deg, #0f172a 0%, #0d9488 50%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    .brand-pill {
        display: inline-flex;
        align-items: center;
        padding: 4px 14px;
        background: linear-gradient(135deg, #e0f2fe 0%, #ccfbf1 100%);
        color: #0f766e;
        border: 1.5px solid #99f6e4;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        box-shadow: 0 4px 14px rgba(153, 246, 228, 0.4);
        animation: floatPill 3.5s ease-in-out infinite alternate;
    }

    @keyframes floatPill {
        0% { transform: translateY(0px); }
        100% { transform: translateY(-4px); }
    }

    /* Sidebar Glassmorphic Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #f0fdfa 100%);
        border-right: 1px solid #ccfbf1;
    }

    .sidebar-section-title {
        font-size: 0.78rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.9px;
        color: #0f766e;
        margin-bottom: 8px;
    }

    .sidebar-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(12px);
        border: 1.5px solid #ccfbf1;
        border-left: 4px solid #0d9488;
        padding: 16px;
        border-radius: 16px;
        margin-top: 10px;
        margin-bottom: 16px;
        box-shadow: 0 4px 16px rgba(13, 148, 136, 0.06);
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .sidebar-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(13, 148, 136, 0.12);
        border-left-color: #3b82f6;
    }

    .sidebar-card h4 {
        color: #0f172a;
        font-size: 1.02rem;
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
        color: #334155;
        font-size: 0.84rem;
        line-height: 1.6;
    }

    /* Interactive "Morphing" Quick Prompt Chips */
    div.stButton > button[kind="secondary"] {
        background: #ffffff !important;
        color: #0f766e !important;
        border: 1.5px solid #99f6e4 !important;
        border-radius: 16px 8px 16px 8px !important;
        font-size: 0.86rem !important;
        font-weight: 600 !important;
        padding: 10px 18px !important;
        box-shadow: 0 4px 14px rgba(153, 246, 228, 0.2) !important;
        transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }

    div.stButton > button[kind="secondary"]:hover {
        background: linear-gradient(135deg, #e0f2fe 0%, #ccfbf1 100%) !important;
        border-color: #3b82f6 !important;
        color: #1e3a8a !important;
        border-radius: 8px 18px 8px 18px !important; /* Shape Morphing on Hover */
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 8px 22px rgba(59, 130, 246, 0.25) !important;
    }
    </style>

    <!-- Top-Right Geometric Triangular Pastel Wave overlay -->
    <div class="top-right-wave-container">
        <svg class="pastel-wave-svg" viewBox="0 0 350 350" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="pastelGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#99f6e4" stop-opacity="0.85"/>
                    <stop offset="50%" stop-color="#bae6fd" stop-opacity="0.9"/>
                    <stop offset="100%" stop-color="#ddd6fe" stop-opacity="0.8"/>
                </linearGradient>
                <linearGradient id="pastelGrad2" x1="0%" y1="100%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.35"/>
                    <stop offset="100%" stop-color="#a7f3d0" stop-opacity="0.4"/>
                </linearGradient>
            </defs>
            <path d="M350,0 L120,0 C170,90 220,130 190,210 C160,290 280,310 350,350 Z" fill="url(#pastelGrad2)" />
            <path d="M350,0 L160,0 C220,70 260,110 230,170 C200,230 300,260 350,300 Z" fill="url(#pastelGrad1)" />
        </svg>
    </div>
""", unsafe_allow_html=True)

# Compact Glassmorphic Sidebar
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

# Minimal Floating Title Header
st.markdown("""
    <div class="brand-title-wrap">
        <h1 class="brand-title">Zahra Mumtaz</h1>
        <span class="brand-pill">✨ Digital AI Clone</span>
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

# Morphing Interactive Sample Prompt Cards
prompt_to_process = None
if len(st.session_state.messages) <= 1:
    st.markdown("<p style='font-weight:600; color:#0f766e; margin-bottom: 12px;'>Suggested Questions:</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    if col1.button("Tell me about Emora 🌸", type="secondary", use_container_width=True):
        prompt_to_process = "Tell me about your final year project Emora."
    if col2.button("What tools do you use? ⚡", type="secondary", use_container_width=True):
        prompt_to_process = "What programming languages and framework tools do you use daily?"
    if col3.button("Signature baking dish? 🍰", type="secondary", use_container_width=True):
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