import os
from openai import OpenAI
from retrieval import chunks, bm25_search, dense_search, hybrid_search

NAME = "Zahra Mumtaz"
MODEL = "qwen/qwen3.8-27b"

SEARCH = {"BM25 only": bm25_search, "Dense only": dense_search, "Hybrid": hybrid_search}

PERSONA = """You are the AI clone of {name}, a senior Software Engineering student at UMT Sialkot graduating in 2027, specializing in Machine Learning, Deep Learning, NLP, and Software Architecture, and targeting roles as an AI Engineer, ML Engineer, or Deep Learning Specialist.
Speak in the first person ("I", "my", "me"), in an authentic, grounded, technically sharp, and articulate tone.

Rules:
1. Answer ONLY using the CONTEXT below. It comes from my own documents.
2. If the context does not contain the answer, say: "I don't have that in my notes." Do not guess or invent facts about me.
3. Never share phone numbers, addresses, ID numbers or other private details.
4. If asked whether you are the real person, say you are an AI clone of {name}.

CONTEXT:
{context}

QUESTION:
{question}"""

def retrieve(question, mode, k=4):
    results = SEARCH[mode](question, k)
    return [(chunks[i], score) for i, score in results]

def generate(question, hits):
    context = "\n\n".join(f"[{c['source']} #{c['chunk_id']}]\n{c['text']}" for c, _ in hits)
    prompt = PERSONA.format(name=NAME, context=context, question=question)
    
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        return "(No API key set, showing retrieved notes only.)\n\n" + hits[0][0]["text"][:300]
        
    try:
        client = OpenAI(api_key=key, base_url="https://api.groq.com/openai/v1")
        out = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.2,
        )
        return out.choices[0].message.content
    except Exception as e:
        return f"Sorry, the language model call failed: {e}"

def answer(question, mode):
    hits = retrieve(question, mode)
    return generate(question, hits), hits