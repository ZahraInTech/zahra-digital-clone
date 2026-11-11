import streamlit as st
from rag_chain import answer

st.set_page_config(
    page_title="Zahra Mumtaz — Digital AI Clone", 
    page_icon="🌊", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injected CSS for Coastal Ocean Aesthetic & Modern Typography
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"], [class*="st-"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }

    .main-header { 
        text-align: center; 
        padding: 24px 20px; 
        background: linear-gradient(135deg, #0f2b3c 0%, #1a4b6e 100%); 
        color: #ffffff; 
        border-radius: 16px; 
        box-shadow: 0 10px 25px -5px rgba(15, 43, 60, 0.15); 
        margin-bottom: 22px; 
        border-bottom: 4px solid #0d9488;
    }

    .main-header h1 { 
        font-size: 2.1rem; 
        font-weight: 700; 
        margin-bottom: 4px; 
        color: #ffffff !important; 
    }

    .main-header p { 
        font-size: 1rem; 
        font-weight: 500;
        color: #e2e8f0 !important; 
        margin: 0; 
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }

    .sidebar-card {
        background: #ffffff;
        border: 1px solid #ccfbf1;
        border-left: 4px solid #0d9488;
        padding: 14px;
        border-radius: 10px;
        margin-bottom: 16px;
    }

    .sidebar-card h4 {
        color: #0f2b3c;
        margin: 0 0 6px 0;
        font-size: 0.98rem;
    }

    .sidebar-card p {
        color: #334155;
        font-size: 0.85rem;
        line-height: 1.4;
        margin: 0;
    }

    /* Quick Prompt Sample Buttons */
    div.stButton > button {
        background: #ffffff !important;
        color: #0f766e !important;
        border: 1.5px solid #0d9488 !important;
        border-radius: 20px !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        padding: 6px 14px !important;
        box-shadow: 0 2px 6px rgba(13, 148, 136, 0.08) !important;
        transition: all 0.2s ease-in-out !important;
    }

    div.stButton > button:hover {
        background: #f0fdfa !important;
        border-color: #0f766e !important;
        transform: translateY(-1px);
    }

    /* Context Snippet Card Styling */
    .snippet-box {
        background-color: #f8fafc;
        border-left: 4px solid #0d9488;
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        font-size: 0.92rem;
        line-height: 1.5;
        color: #1e293b;
    }

    .badge {
        display: inline-block;
        background-color: #e0f2fe;
        color: #0369a1;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Controls & Info
with st.sidebar:
    st.markdown("### ⚙️ Engine Settings")
    mode = st.radio(
        "Retrieval Mode", 
        ["BM25 only", "Dense only", "Hybrid"], 
        index=2,
        help="Hybrid merges lexical BM25 search with dense vector embeddings via Reciprocal Rank Fusion (RRF)."
    )

    st.markdown("---")
    st.markdown("""
        <div class="sidebar-card">
            <h4>🌊 About Zahra's Clone</h4>
            <p>This interactive RAG AI clone indexes Zahra's research papers (Emora, TrashSense), technical software stack, study methodology, and culinary baking recipes.</p>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Main Header
st.markdown("""
    <div class="main-header">
        <h1>Zahra Mumtaz</h1>
        <p>Senior Software Engineering Student &bull; AI Enthusiast</p>
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

# Render Chat Feed
for msg in st.session_state.messages:
    avatar_icon = "🌊" if msg["role"] == "assistant" else None
    with st.chat_message(msg["role"], avatar=avatar_icon):
        st.write(msg["content"])
        
        # Render evidence expander inside response bubble if hits exist
        if msg.get("hits"):
            with st.expander("📚 View RAG Evidence & Context Chunks", expanded=False):
                for idx, (chunk, score) in enumerate(msg["hits"], 1):
                    source_file = chunk.get("source", "Unknown")
                    chunk_id = chunk.get("chunk_id", "N/A")
                    score_fmt = f"{score:.4f}"
                    snippet = chunk.get("text", "").strip()
                    st.markdown(f"""
                        <div class="snippet-box" style="margin-bottom: 10px;">
                            <div>
                                <span class="badge">Source: {source_file}</span>
                                <span class="badge">Chunk #{chunk_id}</span>
                                <span class="badge">RRF Score: {score_fmt}</span>
                            </div>
                            <p style="margin-top: 8px; margin-bottom: 0;">{snippet}</p>
                        </div>
                    """, unsafe_allow_html=True)

# Suggested Questions (visible when only initial greeting is in feed)
prompt_to_process = None

if len(st.session_state.messages) <= 1:
    st.markdown("<p style='font-weight:600; color:#0f2b3c; margin-bottom: 8px;'>Suggested Questions:</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    if col1.button("Tell me about Emora", use_container_width=True):
        prompt_to_process = "Tell me about your final year project Emora."
    if col2.button("What tools do you use?", use_container_width=True):
        prompt_to_process = "What programming languages and framework tools do you use daily?"
    if col3.button("Signature baking dish?", use_container_width=True):
        prompt_to_process = "What is your signature culinary dish or dessert to bake?"

# Bottom Fixed Chat Input
user_input = st.chat_input("Ask Zahra anything...")
if user_input:
    prompt_to_process = user_input

# Execute Query & Append to Chat Feed
if prompt_to_process:
    # Append & display user message
    st.session_state.messages.append({"role": "user", "content": prompt_to_process, "hits": []})
    with st.chat_message("user"):
        st.write(prompt_to_process)

    # Generate assistant response
    with st.chat_message("assistant", avatar="🌊"):
        with st.spinner("Thinking..."):
            reply, hits = answer(prompt_to_process, mode)
            st.write(reply)

            if hits:
                with st.expander("📚 View RAG Evidence & Context Chunks", expanded=False):
                    for idx, (chunk, score) in enumerate(hits, 1):
                        source_file = chunk.get("source", "Unknown")
                        chunk_id = chunk.get("chunk_id", "N/A")
                        score_fmt = f"{score:.4f}"
                        snippet = chunk.get("text", "").strip()
                        st.markdown(f"""
                            <div class="snippet-box" style="margin-bottom: 10px;">
                                <div>
                                    <span class="badge">Source: {source_file}</span>
                                    <span class="badge">Chunk #{chunk_id}</span>
                                    <span class="badge">RRF Score: {score_fmt}</span>
                                </div>
                                <p style="margin-top: 8px; margin-bottom: 0;">{snippet}</p>
                            </div>
                        """, unsafe_allow_html=True)

            st.session_state.messages.append({"role": "assistant", "content": reply, "hits": hits})
            st.rerun()