import os, re, glob
import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

DATA_DIR = "data"
CHUNK_WORDS, OVERLAP = 250, 40

def load_chunks():
    chunks = []
    for path in sorted(glob.glob(os.path.join(DATA_DIR, "*"))):
        if not path.endswith((".md", ".txt")):
            continue
        words = open(path, encoding="utf-8").read().split()
        start, cid = 0, 0
        while start < len(words):
            text = " ".join(words[start:start + CHUNK_WORDS])
            chunks.append({"source": os.path.basename(path), "chunk_id": cid, "text": text})
            cid += 1
            if start + CHUNK_WORDS >= len(words):
                break
            start += CHUNK_WORDS - OVERLAP
    return chunks

def tokenize(text):
    return re.findall(r"\w+", text.lower())

chunks = load_chunks()
bm25 = BM25Okapi([tokenize(c["text"]) for c in chunks])

model = SentenceTransformer("all-MiniLM-L6-v2")
if os.path.exists("embeddings.npy"):
    emb = np.load("embeddings.npy")
else:
    emb = model.encode([c["text"] for c in chunks], normalize_embeddings=True)
    np.save("embeddings.npy", emb)

def bm25_search(q, k=5):
    scores = bm25.get_scores(tokenize(q))
    idx = np.argsort(scores)[::-1][:k]
    return [(int(i), float(scores[i])) for i in idx]

def dense_search(q, k=5):
    qv = model.encode([q], normalize_embeddings=True)[0]
    scores = emb @ qv
    idx = np.argsort(scores)[::-1][:k]
    return [(int(i), float(scores[i])) for i in idx]

def hybrid_search(q, k=5, pool=20):
    rrf = {}
    for results in (bm25_search(q, pool), dense_search(q, pool)):
        for rank, (i, _) in enumerate(results, start=1):
            rrf[i] = rrf.get(i, 0) + 1 / (60 + rank)
    top = sorted(rrf.items(), key=lambda x: x[1], reverse=True)[:k]
    return [(i, s) for i, s in top]

if __name__ == "__main__":
    q = input("Question: ")
    for name, fn in [("BM25", bm25_search), ("DENSE", dense_search), ("HYBRID", hybrid_search)]:
        print(f"\n--- {name} ---")
        for i, s in fn(q, 3):
            c = chunks[i]
            print(f"{s:.4f} | {c['source']} #{c['chunk_id']} | {c['text'][:100]}...")