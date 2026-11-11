import streamlit as st
from rag_chain import answer

st.set_page_config(
    page_title="Zahra Mumtaz — Digital AI Clone", 
    page_icon="🌊", 
    layout="wide"
)

# Injected CSS for Coastal Ocean Aesthetic & Plus Jakarta Sans Font
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"], [class*="st-"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }

    .header-card { 
        text-align: center; 
        padding: 28px 20px; 
        background: linear-gradient(135deg, #0f2b3c 0%, #1a4b6e 100%); 
        color: #ffffff; 
        border-radius: 16px; 
        box-shadow: 0 10px 25px -5px rgba(15, 43, 60, 0.15); 
        margin-bottom: 20px; 
        border-bottom: 4px solid #0d9488;
    }

    .header-card h1 { 
        font-size: 2.3rem; 
        font-weight: 700; 
        margin-bottom: 6px; 
        letter-spacing: -0.5px; 
        color: #ffffff !important; 
    }

    .header-card p { 
        font-size: 1.05rem; 
        font-weight: 500;
        color: #e2e8f0 !important; 
        margin: 0; 
    }

    .disclaimer-badge { 
        background: #f0fdfa; 
        color: #134e4a; 
        padding: 12px 18px; 
        border-radius: 12px; 
        font-size: 0.9rem; 
        font-weight: 500;
        text-align: center; 
        margin-bottom: 22px; 
        border: 1px solid #ccfbf1; 
    }

    /* Main Teal Action Button Styling */
    div.stButton > button[kind="primary"], div.stButton > button {
        background: linear-gradient(135deg, #0d9488 0%, #0f766e 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(13, 148, 136, 0.25) !important;
        transition: all 0.2s ease-in-out !important;
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #0f766e 0%, #115e59 100%) !important;
        transform: translateY(-1px);
    }
    </style>
""", unsafe_allow_html=True)

# Header & Disclaimer
st.markdown("""
    <div class="header-card">
        <h1>Zahra Mumtaz</h1>
        <p>Senior Software Engineering Student &bull; AI Enthusiast</p>
    </div>
    <div class="disclaimer-badge">
        <b>Interactive RAG AI Clone</b> — Ask about my academic research (Emora, TrashSense), technical stack, study methodology, or culinary baking!
    </div>
""", unsafe_allow_html=True)

if "user_query" not in st.session_state:
    st.session_state["user_query"] = ""

col1, col2 = st.columns([3, 1])

with col1:
    question = st.text_input(
        "Your Question", 
        value=st.session_state["user_query"],
        placeholder="e.g., Tell me about your final year project Emora..."
    )

with col2:
    mode = st.radio(
        "Retrieval Mode", 
        ["BM25 only", "Dense only", "Hybrid"], 
        index=2
    )

submit = st.button("Ask Zahra", use_container_width=True)

# Quick Questions
st.markdown("##### Quick Questions to Try")
q_col1, q_col2, q_col3 = st.columns(3)

if q_col1.button("Tell me about Emora"):
    st.session_state["user_query"] = "Tell me about your final year project Emora."
    st.rerun()

if q_col2.button("What tools do you use?"):
    st.session_state["user_query"] = "What programming languages and framework tools do you use daily?"
    st.rerun()

if q_col3.button("Signature baking dish?"):
    st.session_state["user_query"] = "What is your signature culinary dish or dessert to bake?"
    st.rerun()

# Execution
if submit and question.strip():
    with st.spinner("Thinking..."):
        reply, hits = answer(question, mode)
        st.markdown("### Zahra's Answer")
        st.write(reply)
        
        st.markdown("### Hybrid RAG Evidence & Context Chunks")
        rows = [
            {
                "Source File": c["source"], 
                "Chunk ID": c["chunk_id"], 
                "Score": round(score, 4), 
                "Matched Context Snippet": c["text"][:300] + "..."
            } 
            for c, score in hits
        ]
        st.dataframe(rows, use_container_width=True)
elif submit:
    st.warning("Please enter a question to start chatting!")