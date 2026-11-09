import gradio as gr
from rag_chain import answer

def ask(question, mode):
    if not question.strip():
        return "Please enter a question to start chatting!", []
    reply, hits = answer(question, mode)
    rows = [[c["source"], c["chunk_id"], round(score, 4), c["text"][:300] + "..."] for c, score in hits]
    return reply, rows

# Coastal Ocean Aesthetic & Modern Typography Styling
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

* {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
}

#main-container { 
    max-width: 940px; 
    margin: 0 auto; 
    padding: 12px; 
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
    letter-spacing: 0.2px;
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

.ask-btn { 
    background: linear-gradient(135deg, #0d9488 0%, #0f766e 100%) !important; 
    color: #ffffff !important; 
    font-weight: 600 !important; 
    border-radius: 10px !important; 
    border: none !important;
    box-shadow: 0 4px 12px rgba(13, 148, 136, 0.25) !important;
    transition: all 0.2s ease-in-out !important;
}

.ask-btn:hover {
    background: linear-gradient(135deg, #0f766e 0%, #115e59 100%) !important;
    transform: translateY(-1px);
}
"""

with gr.Blocks(
    css=custom_css, 
    title="Zahra Mumtaz — Digital AI Clone", 
    theme=gr.themes.Soft(primary_hue="teal", neutral_hue="slate")
) as demo:
    with gr.Column(elem_id="main-container"):
        gr.HTML("""
            <div class="header-card">
                <h1>Zahra Mumtaz</h1>
                <p>Senior Software Engineering Student &bull; AI Enthusiast</p>
            </div>
            <div class="disclaimer-badge">
                <b>Interactive RAG AI Clone</b> — Ask about my academic research (Emora, TrashSense), technical stack, study methodology, or culinary baking!
            </div>
        """)
        
        with gr.Row():
            with gr.Column(scale=3):
                q = gr.Textbox(
                    label="Your Question", 
                    placeholder="e.g., Tell me about your final year project Emora...",
                    lines=2
                )
            with gr.Column(scale=1):
                mode = gr.Radio(
                    ["BM25 only", "Dense only", "Hybrid"], 
                    value="Hybrid", 
                    label="Retrieval Mode"
                )
        
        btn = gr.Button("Ask Zahra", variant="primary", elem_classes=["ask-btn"])
        
        ans = gr.Textbox(label="Zahra's Answer", lines=6, placeholder="Response will appear here...")
        
        table = gr.Dataframe(
            headers=["Source File", "Chunk ID", "Score", "Matched Context Snippet"], 
            label="Hybrid RAG Evidence & Context Chunks", 
            wrap=True
        )
        
        gr.Examples(
            examples=[
                ["Tell me about your final year project Emora.", "Hybrid"],
                ["What programming languages and framework tools do you use daily?", "Hybrid"],
                ["What is your signature culinary dish or dessert to bake?", "Hybrid"],
                ["How do you approach software engineering documentation and study workflows?", "Hybrid"],
                ["What hackathons and awards have you achieved?", "Hybrid"]
            ],
            inputs=[q,mode],
            label="Quick Questions to Try"
        )

        btn.click(ask, [q, mode], [ans, table])
        q.submit(ask, [q, mode], [ans, table])

if __name__ == "__main__":
    demo.launch()