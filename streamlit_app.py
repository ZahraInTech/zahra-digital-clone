import re
import streamlit as st
from rag_chain import answer

st.set_page_config(
    page_title="Zahra — Digital AI Clone", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Bespoke Glass-Ring SVG Vector Avatars (Delicate thin-stroke design)
AVATAR_ASSISTANT = "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'><circle cx='20' cy='20' r='19' fill='%23f0fdfa' stroke='%230d9488' stroke-width='1.5'/><path d='M11 18c2.2 0 3.2-1.8 5.5-1.8s3.3 1.8 5.5 1.8 3.3-1.8 5.5-1.8' stroke='%230f766e' stroke-width='2' fill='none' stroke-linecap='round'/><path d='M11 23c2.2 0 3.2-1.8 5.5-1.8s3.3 1.8 5.5 1.8 3.3-1.8 5.5-1.8' stroke='%230d9488' stroke-width='1.5' stroke-opacity='0.75' fill='none' stroke-linecap='round'/></svg>"
AVATAR_USER = "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'><circle cx='20' cy='20' r='19' fill='%23f0f9ff' stroke='%230284c7' stroke-width='1.5'/><path d='M20 17.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7zm0 2.5c-3.8 0-7 1.8-7 4v1h14v-1c0-2.2-3.2-4-7-4z' fill='%230284c7'/></svg>"

# CSS for Full-Height Sea Backdrop, Cohesive Header, and Single-Capsule Input Bar
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, p, h1, h2, h3, h4, h5, h6, span, label, input, textarea, button {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Full-Height Coastal Ocean Backdrop */
    [data-testid="stAppViewContainer"] {
        background: 
            linear-gradient(180deg, rgba(235, 248, 250, 0.45) 0%, rgba(255, 255, 255, 0.65) 50%, rgba(204, 251, 241, 0.75) 100%),
            url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=2000&auto=format&fit=crop') !important;
        background-size: cover !important;
        background-position: center top !important;
        background-attachment: fixed !important;
    }

    /* 100% Transparent Bottom Dock Containers */
    [data-testid="stBottom"], [data-testid="stBottom"] > div, footer, header {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Top-Left Organic Glass Wave Curve */
    .top-left-glass-wave {
        position: fixed !important;
        top: 0px !important;
        left: 0px !important;
        width: 380px;
        height: 280px;
        pointer-events: none;
        z-index: 1;
    }

    /* Bottom-Right Organic Glass Wave Curve */
    .bottom-right-glass-wave {
        position: fixed !important;
        bottom: 0px !important;
        right: 0px !important;
        width: 460px;
        height: 320px;
        pointer-events: none;
        z-index: 1;
    }

    /* Cohesive Header Layout */
    .header-container {
        margin-top: 10px;
        margin-bottom: 24px;
        position: relative;
        z-index: 10;
    }

    .name-title-wrap {
        display: flex;
        align-items: baseline;
        gap: 8px;
    }

    .meet-prefix {
        font-size: 2.3rem;
        font-weight: 500;
        color: #0d9488;
        letter-spacing: -0.4px;
    }

    .name-text {
        font-size: 2.7rem;
        font-weight: 800;
        color: #0f2b3c;
        margin: 0;
        letter-spacing: -0.8px;
    }

    .heart-icon {
        font-size: 1.8rem;
        color: #0d9488;
        font-weight: 400;
    }

    .sub-text {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.8px;
        color: #64748b;
        margin-top: 4px;
    }

    /* Glassmorphic Chat Cards */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.88) !important;
        backdrop-filter: blur(16px) !important;
        border-radius: 22px !important;
        padding: 20px 24px !important;
        margin-bottom: 18px !important;
        border: 1px solid rgba(255, 255, 255, 0.9) !important;
        box-shadow: 0 10px 30px -5px rgba(13, 148, 136, 0.08), 0 4px 12px rgba(0, 0, 0, 0.03) !important;
    }

    /* Refined Chat Avatar Sizing & Border Drop Shadow */
    [data-testid="stChatMessage"] img {
        width: 40px !important;
        height: 40px !important;
        border-radius: 50% !important;
        filter: drop-shadow(0 2px 6px rgba(13, 148, 136, 0.12));
    }

    /* RAG Evidence Expander Pill Button */
    [data-testid="stExpander"] {
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
        margin-top: 10px !important;
    }

    [data-testid="stExpander"] details {
        border: 1px solid rgba(203, 213, 225, 0.6) !important;
        border-radius: 20px !important;
        background: rgba(255, 255, 255, 0.95) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
        padding: 4px 12px !important;
    }

    [data-testid="stExpander"] summary {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: #475569 !important;
    }

    /* Floating Glass Chat Input Capsule (Single Seamless Outer Border) */
    [data-testid="stChatInput"] {
        background: rgba(255, 255, 255, 0.85) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 40px !important;
        border: 1.5px solid rgba(255, 255, 255, 0.9) !important;
        box-shadow: 0 12px 35px rgba(13, 148, 136, 0.15) !important;
        padding: 4px 8px !important;
        margin-bottom: 8px !important;
    }

    /* Remove inner nested box borders completely */
    [data-testid="stChatInput"] > div,
    [data-testid="stChatInput"] div[data-baseweb="input"],
    [data-testid="stChatInput"] textarea {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
    }

    [data-testid="stChatInput"] textarea {
        color: #0f2b3c !important;
        font-size: 0.95rem !important;
    }

    /* Circular Send Button */
    [data-testid="stChatInput"] button {
        background: #0f766e !important;
        color: #ffffff !important;
        border-radius: 50% !important;
        border: none !important;
    }

    /* Sidebar Glassmorphic Styling */
    [data-testid="stSidebar"] {
        background: rgba(248, 250, 252, 0.85) !important;
        backdrop-filter: blur(16px) !important;
        border-right: 1px solid rgba(203, 213, 225, 0.5) !important;
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
        border-left: 4px solid #0d9488;
        padding: 16px;
        border-radius: 14px;
        margin-top: 10px;
        margin-bottom: 16px;
        box-shadow: 0 4px 16px rgba(13, 148, 136, 0.06);
    }

    .sidebar-card h4 {
        color: #0f2b3c;
        font-size: 1rem;
        font-weight: 700;
        margin: 0 0 6px 0;
    }

    .sidebar-card p {
        color: #475569;
        font-size: 0.85rem;
        line-height: 1.5;
        margin-bottom: 8px;
    }

    .sidebar-list {
        margin: 0;
        padding-left: 16px;
        color: #334155;
        font-size: 0.83rem;
        line-height: 1.6;
    }

    /* Suggested Question Buttons */
    div.stButton > button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.9) !important;
        color: #0f766e !important;
        border: 1.5px solid #99f6e4 !important;
        border-radius: 20px !important;
        font-size: 0.86rem !important;
        font-weight: 600 !important;
        padding: 10px 18px !important;
        box-shadow: 0 4px 14px rgba(13, 148, 136, 0.08) !important;
        transition: all 0.3s ease-in-out !important;
    }

    div.stButton > button[kind="secondary"]:hover {
        background: #f0fdfa !important;
        border-color: #0d9488 !important;
        transform: translateY(-2px) !important;
    }
    </style>

    <!-- Top-Left Glass Wave Overlay -->
    <svg class="top-left-glass-wave" viewBox="0 0 380 280" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M0,0 L260,0 C180,80 220,160 140,220 C60,280 0,220 0,280 Z" fill="url(#waveGradTL)" opacity="0.45"/>
        <defs>
            <linearGradient id="waveGradTL" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#2dd4bf"/>
                <stop offset="100%" stop-color="#38bdf8"/>
            </linearGradient>
        </defs>
    </svg>

    <!-- Bottom-Right Glass Wave Overlay -->
    <svg class="bottom-right-glass-wave" viewBox="0 0 460 320" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M460,320 L180,320 C240,240 280,180 360,120 C440,60 460,0 460,0 Z" fill="url(#waveGradBR)" opacity="0.35"/>
        <defs>
            <linearGradient id="waveGradBR" x1="100%" y1="100%" x2="0%" y2="0%">
                <stop offset="0%" stop-color="#0d9488"/>
                <stop offset="100%" stop-color="#7dd3fc"/>
            </linearGradient>
        </defs>
    </svg>
""", unsafe_allow_html=True)

# Helper Functions
def clean_text_snippet(raw_text):
    return re.sub(r'^#+\s*', '', str(raw_text).strip())

def parse_hit_item(item):
    if isinstance(item, tuple) and len(item) > 0:
        chunk_dict = item[0] if isinstance(item[0], dict) else {}
        score = item[1] if len(item) > 1 and isinstance(item[1], (int, float)) else 0.0
        return chunk_dict, score
    elif isinstance(item, dict):
        return item, 0.0
    return {}, 0.0

# Compact Sidebar
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

# Cohesive Unified Headline Header
st.markdown("""
    <div class="header-container">
        <div class="name-title-wrap">
            <h1 class="name-text"><span class="meet-prefix">Meet</span> Zahra Mumtaz</h1>
            <span class="heart-icon">&#9825;</span>
        </div>
        <div class="sub-text">AI DIGITAL CLONE &bull; ALWAYS HERE FOR YOU</div>
    </div>
""", unsafe_allow_html=True)

# Session State Initialization (Starts clean)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render Chat Feed
for msg in st.session_state.messages:
    avatar_icon = AVATAR_ASSISTANT if msg["role"] == "assistant" else AVATAR_USER
    with st.chat_message(msg["role"], avatar=avatar_icon):
        st.markdown(msg["content"])
        
        if msg.get("hits"):
            with st.expander("&darr; View RAG Evidence & Context Chunks", expanded=False):
                for idx, raw_item in enumerate(msg["hits"], 1):
                    chunk, score = parse_hit_item(raw_item)
                    source_file = chunk.get("source", "Unknown")
                    chunk_id = chunk.get("chunk_id", "N/A")
                    snippet = clean_text_snippet(chunk.get("text", ""))
                    score_fmt = f"{score:.4f}" if score else "N/A"
                    
                    st.markdown(f"**Match #{idx}** | `Source: {source_file}` | `Chunk: #{chunk_id}` | `Score: {score_fmt}`")
                    st.code(snippet, language=None, wrap_lines=True)

# Suggested Questions Cards (Disappears once chat starts)
prompt_to_process = None
if len(st.session_state.messages) == 0:
    col1, col2, col3 = st.columns(3)
    if col1.button("Tell me about Emora", type="secondary", use_container_width=True):
        prompt_to_process = "Tell me about your final year project Emora."
    if col2.button("What tools do you use?", type="secondary", use_container_width=True):
        prompt_to_process = "What programming languages and framework tools do you use daily?"
    if col3.button("Signature baking dish?", type="secondary", use_container_width=True):
        prompt_to_process = "What is your signature culinary dish or dessert to bake?"

# Bottom Pinned Chat Input Bar
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
            reply, hits_data = answer(prompt_to_process, backend_mode)
            st.markdown(reply)

            hits_list = hits_data if hits_data else []

            if hits_list:
                with st.expander("&darr; View RAG Evidence & Context Chunks", expanded=False):
                    for idx, raw_item in enumerate(hits_list, 1):
                        chunk, score = parse_hit_item(raw_item)
                        source_file = chunk.get("source", "Unknown")
                        chunk_id = chunk.get("chunk_id", "N/A")
                        snippet = clean_text_snippet(chunk.get("text", ""))
                        score_fmt = f"{score:.4f}" if score else "N/A"
                        
                        st.markdown(f"**Match #{idx}** | `Source: {source_file}` | `Chunk: #{chunk_id}` | `Score: {score_fmt}`")
                        st.code(snippet, language=None, wrap_lines=True)

            st.session_state.messages.append({"role": "assistant", "content": reply, "hits": hits_list})
            st.rerun()