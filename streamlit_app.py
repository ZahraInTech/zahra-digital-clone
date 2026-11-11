import re
import streamlit as st
from rag_chain import answer

st.set_page_config(
    page_title="Zahra — Digital AI Clone", 
    page_icon="🌊", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Deep Coastal Ocean Palette + Expanded Animated Wave SVG CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, p, h1, h2, h3, h4, h5, h6, span, label, input, textarea, button {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Expanded Top-Right Coastal Wave (Organic Tide Motion) */
    .top-right-wave-container {
        position: fixed;
        top: 0;
        right: 0;
        width: 540px;
        height: 540px;
        pointer-events: none;
        z-index: 99999;
        overflow: hidden;
    }

    .coastal-wave-svg {
        width: 100%;
        height: 100%;
        filter: drop-shadow(-12px 18px 35px rgba(13, 148, 136, 0.22));
        transform-origin: top right;
        animation: seaTideFlow 11s ease-in-out infinite alternate;
    }

    /* Organic Ocean Tide Animation */
    @keyframes seaTideFlow {
        0% {
            transform: scale(1) rotate(0deg) translateY(0px);
        }
        50% {
            transform: scale(1.05) rotate(-2deg) translateY(-14px);
        }
        100% {
            transform: scale(0.98) rotate(1.5deg) translateY(10px);
        }
    }

    /* Clean Standalone Header (No Oval Badge) */
    .brand-title-wrap {
        display: flex;
        align-items: center;
        margin-top: 10px;
        margin-bottom: 22px;
    }

    .brand-title {
        font-size: 2.6rem;
        font-weight: 800;
        letter-spacing: -0.8px;
        background: linear-gradient(135deg, #0f2b3c 0%, #0d9488 45%, #0284c7 80%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    /* Sidebar Glassmorphic Coastal Styling */
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
        background: rgba(255, 255, 255, 0.88);
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
        border-left-color: #0284c7;
    }

    .sidebar-card h4 {
        color: #0f2b3c;
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

    /* Morphing Quick Prompt Chips */
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
        background: linear-gradient(135deg, #f0fdfa 0%, #e0f2fe 100%) !important;
        border-color: #0284c7 !important;
        color: #0369a1 !important;
        border-radius: 8px 18px 8px 18px !important;
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 8px 22px rgba(2, 132, 199, 0.2) !important;
    }
    </style>

    <!-- Expanded Rich Coastal Wave SVG Overlay -->
    <div class="top-right-wave-container">
        <svg class="coastal-wave-svg" viewBox="0 0 540 540" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <!-- Outer Mist Layer -->
                <linearGradient id="crestGrad" x1="0%" y1="100%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="#ccfbf1" stop-opacity="0.5"/>
                    <stop offset="100%" stop-color="#7dd3fc" stop-opacity="0.65"/>
                </linearGradient>

                <!-- Middle Coastal Aqua Layer -->
                <linearGradient id="coastalAquaGrad" x1="100%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.75"/>
                    <stop offset="55%" stop-color="#99f6e4" stop-opacity="0.85"/>
                    <stop offset="100%" stop-color="#e0f2fe" stop-opacity="0.6"/>
                </linearGradient>

                <!-- Deep Sea Ocean Core Layer -->
                <linearGradient id="deepSeaGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#0f2b3c" stop-opacity="0.9"/>
                    <stop offset="45%" stop-color="#0d9488" stop-opacity="0.8"/>
                    <stop offset="100%" stop-color="#0284c7" stop-opacity="0.7"/>
                </linearGradient>
            </defs>

            <!-- Layer 1: Outer Foam Crest -->
            <path d="M540,0 L130,0 C210,140 320,190 240,340 C160,490 390,490 540,540 Z" fill="url(#crestGrad)" />
            <!-- Layer 2: Mid-Tide Aqua -->
            <path d="M540,0 L190,0 C270,120 360,160 290,290 C220,420 440,430 540,490 Z" fill="url(#coastalAquaGrad)" />
            <!-- Layer 3: Deep Sea Core -->
            <path d="M540,0 L260,0 C340,95 410,130 350,230 C290,330 470,360 540,420 Z" fill="url(#deepSeaGrad)" />
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

# Standalone Name Header (No Oval Badge)
st.markdown("""
    <div class="brand-title-wrap">
        <h1 class="brand-title">Zahra Mumtaz</h1>
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

# Morphing Sample Prompt Cards
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