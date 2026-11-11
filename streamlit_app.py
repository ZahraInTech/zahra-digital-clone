import re
import streamlit as st
from rag_chain import answer

st.set_page_config(
    page_title="Zahra — Digital AI Clone", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom SVG Icons (Encoded as Data URIs for crisp vector rendering)
AVATAR_ASSISTANT = "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23c5a059' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M2 6c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.5 0 2.5 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1'/><path d='M2 12c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1'/><path d='M2 18c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1'/></svg>"
AVATAR_USER = "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%230d9488' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2'/><circle cx='12' cy='7' r='4'/></svg>"

# Luxury Emerald, Aquamarine & Sand Gold Palette CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, p, h1, h2, h3, h4, h5, h6, span, label, input, textarea, button {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Soft Luxury Coastal Canvas Background (Emerald + Aquamarine + Sand Gold Glow) */
    [data-testid="stAppViewContainer"] {
        background: 
            radial-gradient(circle at 100% 0%, rgba(197, 160, 89, 0.22) 0%, rgba(94, 234, 212, 0.2) 25%, rgba(13, 148, 136, 0.12) 50%, transparent 75%),
            radial-gradient(circle at 85% 20%, rgba(203, 213, 225, 0.3) 0%, transparent 45%),
            #ffffff !important;
    }

    /* Fixed Top-Right Viewport Wave Graphic (Emerald Teal & Metallic Sand Gold) */
    .top-right-wave-box {
        position: fixed !important;
        top: 0px !important;
        right: 0px !important;
        width: 440px;
        height: 360px;
        pointer-events: none;
        z-index: 9999;
        overflow: hidden;
    }

    .coastal-wave-svg {
        width: 100%;
        height: 100%;
        filter: drop-shadow(-8px 12px 24px rgba(197, 160, 89, 0.18));
        transform-origin: top right;
        animation: seaTideFlow 10s ease-in-out infinite alternate;
    }

    @keyframes seaTideFlow {
        0% {
            transform: scale(1) rotate(0deg) translateY(0px);
        }
        50% {
            transform: scale(1.04) rotate(-1.8deg) translateY(-8px);
        }
        100% {
            transform: scale(0.98) rotate(1.2deg) translateY(6px);
        }
    }

    /* Bespoke Header Gradient (Deep Emerald -> Aquamarine -> Sand Gold) */
    .brand-title-wrap {
        position: relative;
        z-index: 20;
        margin-top: 4px;
        margin-bottom: 22px;
    }

    .brand-title {
        font-size: 2.7rem;
        font-weight: 800;
        letter-spacing: -0.8px;
        background: linear-gradient(135deg, #064e3b 0%, #0d9488 40%, #0284c7 70%, #c5a059 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    /* Glassmorphic Sidebar with Sand Gold Accents */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #f0fdfa 100%);
        border-right: 1px solid #e2e8f0;
    }

    .sidebar-section-title {
        font-size: 0.75rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.1px;
        color: #0f766e;
        margin-bottom: 8px;
    }

    .sidebar-card {
        background: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(12px);
        border: 1px solid #e2e8f0;
        border-left: 4px solid #c5a059; /* Metallic Sand Gold Accent */
        padding: 16px;
        border-radius: 14px;
        margin-top: 10px;
        margin-bottom: 16px;
        box-shadow: 0 4px 16px rgba(197, 160, 89, 0.08);
    }

    .sidebar-card h4 {
        color: #064e3b;
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

    /* Luxury Prompt Chips (Sand Gold Border + Hover Transformation) */
    div.stButton > button[kind="secondary"] {
        background: #ffffff !important;
        color: #0f766e !important;
        border: 1.5px solid #c5a059 !important;
        border-radius: 14px !important;
        font-size: 0.86rem !important;
        font-weight: 600 !important;
        padding: 10px 18px !important;
        box-shadow: 0 4px 14px rgba(197, 160, 89, 0.12) !important;
        transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }

    div.stButton > button[kind="secondary"]:hover {
        background: linear-gradient(135deg, #fefce8 0%, #f0fdfa 100%) !important;
        border-color: #0d9488 !important;
        color: #064e3b !important;
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: 0 8px 20px rgba(13, 148, 136, 0.18) !important;
    }
    </style>

    <!-- Top-Right Fixed Wave SVG Overlay -->
    <div class="top-right-wave-box">
        <svg class="coastal-wave-svg" viewBox="0 0 440 360" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="sandGoldGrad" x1="0%" y1="100%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="#c5a059" stop-opacity="0.45"/>
                    <stop offset="100%" stop-color="#5eead4" stop-opacity="0.6"/>
                </linearGradient>
                <linearGradient id="aquamarineGrad" x1="100%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stop-color="#0d9488" stop-opacity="0.75"/>
                    <stop offset="100%" stop-color="#2dd4bf" stop-opacity="0.8"/>
                </linearGradient>
                <linearGradient id="emeraldNavyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#064e3b" stop-opacity="0.9"/>
                    <stop offset="100%" stop-color="#0f766e" stop-opacity="0.85"/>
                </linearGradient>
            </defs>
            <path d="M440,0 L60,0 C140,80 250,110 170,210 C90,310 300,310 440,360 Z" fill="url(#sandGoldGrad)" />
            <path d="M440,0 L120,0 C180,70 270,90 210,170 C150,250 340,260 440,310 Z" fill="url(#aquamarineGrad)" />
            <path d="M440,0 L180,0 C240,55 310,70 270,130 C220,190 370,210 440,260 Z" fill="url(#emeraldNavyGrad)" />
        </svg>
    </div>
""", unsafe_allow_html=True)

# Compact Glassmorphic Sidebar
with st.sidebar:
    st.markdown("<p class='sidebar-section-title'>Retrieval Engine</p>", unsafe_allow_html=True)
    mode = st.radio(
        "Search Mode", 
        ["BM25 Lexical", "Dense Vector", "Hybrid"], 
        index=2,
        help="Hybrid merges lexical BM25 search with dense vector embeddings."
    )

    st.markdown("---")
    
    st.markdown("<p class='sidebar-section-title'>Digital Profile</p>", unsafe_allow_html=True)
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

    if st.button("Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Clean Title Header
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

# Render Chat Feed with Custom Vector SVG Avatars
for msg in st.session_state.messages:
    avatar_icon = AVATAR_ASSISTANT if msg["role"] == "assistant" else AVATAR_USER
    with st.chat_message(msg["role"], avatar=avatar_icon):
        st.markdown(msg["content"])
        
        if msg.get("hits"):
            with st.expander("View RAG Evidence & Context Chunks", expanded=False):
                for idx, (chunk, score) in enumerate(msg["hits"], 1):
                    source_file = chunk.get("source", "Unknown")
                    chunk_id = chunk.get("chunk_id", "N/A")
                    score_fmt = f"{score:.4f}"
                    snippet = clean_text_snippet(chunk.get("text", ""))
                    
                    st.markdown(f"**Match #{idx}** | `Source: {source_file}` | `Chunk: #{chunk_id}` | `Score: {score_fmt}`")
                    st.code(snippet, language=None, wrap_lines=True)

# Sample Prompt Chips
prompt_to_process = None
if len(st.session_state.messages) <= 1:
    st.markdown("<p style='font-weight:600; color:#0f766e; margin-bottom: 12px;'>Suggested Questions:</p>", unsafe_allow_html=True)
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
    with st.chat_message("user", avatar=AVATAR_USER):
        st.markdown(prompt_to_process)

    with st.chat_message("assistant", avatar=AVATAR_ASSISTANT):
        with st.spinner("Searching knowledge base..."):
            reply, hits = answer(prompt_to_process, backend_mode)
            st.markdown(reply)

            if hits:
                with st.expander("View RAG Evidence & Context Chunks", expanded=False):
                    for idx, (chunk, score) in enumerate(hits, 1):
                        source_file = chunk.get("source", "Unknown")
                        chunk_id = chunk.get("chunk_id", "N/A")
                        score_fmt = f"{score:.4f}"
                        snippet = clean_text_snippet(chunk.get("text", ""))
                        
                        st.markdown(f"**Match #{idx}** | `Source: {source_file}` | `Chunk: #{chunk_id}` | `Score: {score_fmt}`")
                        st.code(snippet, language=None, wrap_lines=True)

            st.session_state.messages.append({"role": "assistant", "content": reply, "hits": hits})
            st.rerun()