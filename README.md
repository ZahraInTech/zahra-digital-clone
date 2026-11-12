# Zahra Mumtaz — Digital AI Clone

> **Disclaimer:** This is an AI clone of Zahra Mumtaz, not the real person. All responses are generated strictly from personal documents, project write-ups, and notes authored by Zahra.

An interactive Hybrid Retrieval-Augmented Generation (RAG) chatbot that answers questions in first person as Zahra Mumtaz. The system combines lexical keyword search (**BM25**) and semantic vector search (**Sentence Transformers**) via **Reciprocal Rank Fusion (RRF)**, passing the top-ranked passages to a Groq-hosted LLM constrained to answer solely from retrieved context.

**Live App:** [Zahra Mumtaz — Digital AI Clone](https://zahra-digital-clone.streamlit.app)  
**Source Repository:** https://github.com/ZahraInTech/zahra-digital-clone

---

## System Architecture

- **LLM Inference Engine:** Groq API (`qwen-2.5-32b`) with a grounded first-person persona prompt
- **Lexical Retriever:** `rank_bm25` (`BM25Okapi`) over tokenized text chunks
- **Dense Retriever:** `sentence-transformers` (`all-MiniLM-L6-v2`) with precomputed `.npy` chunk embeddings and NumPy cosine similarity
- **Hybrid Fusion:** Reciprocal Rank Fusion (RRF) merging lexical and semantic rankings
- **Frontend UI:** Streamlit with custom glassmorphic styling, retrieval mode selector (`BM25 Lexical`, `Dense Vector`, `Hybrid`), and expandable RAG evidence cards

---

## 1. Knowledge Base & Chunking

The knowledge base in `data/` consists of **7 Markdown documents** (~18 pages total) authored specifically for this clone, covering all four required content categories while excluding any private contact details, IDs, or sensitive records:

1. **`01_bio_and_education.md` (Factual Bio & CV):** Academic background in BS Software Engineering at the University of Management and Technology (UMT) Sialkot, core computer science coursework, and semester academic awards.
2. **`02_technical_stack_and_workflows.md` (Study & Engineering Notes):** Daily software development stack (Python, C++, PyTorch, Scikit-learn, OpenCV, LangGraph, FastAPI, Git), clean documentation principles, and exam revision workflows.
3. **`03_emora_fyp.md` (Long-Form Project Write-up):** Problem formulation, KIDO dataset pipeline, vision and language backbones (ResNet-50, DenseNet-121, ViT, RoBERTa), Grad-CAM explainability, and multimodal fusion experiments for the **Emora** Final Year Project.
4. **`04_trashsense_research.md` (Long-Form Research Write-up):** Architecture and evaluation of **Trash-Sense**, a calibrated and guarded Vision-LLM framework for household waste classification and disposal guidance.
5. **`05_software_projects.md` (Factual Technical Portfolio):** Implementation details for **File Vault** (hybrid AES-256-GCM and RSA-2048 OAEP desktop encryption utility) and **Repo-Tutor** (multi-agent codebase onboarding copilot).
6. **`06_personality_hobbies_and_culinary.md` (Personality & Opinions):** Favorite animated films (Studio Ghibli's *When Marnie Was There*, *The Wind Rises*, *Howl's Moving Castle*, and *Turbo*), minimalist design inspiration, indoor plant care, and scratch baking/cooking recipes (Tiramisu with homemade mascarpone, Saffron Tres Leches, Sticky Toffee Pudding, and Pink/Mixed Sauce Pasta).
7. **`07_faqs.md` (First-Person FAQ):** 29 first-person questions and answers capturing Zahra's authentic voice, advice for junior software engineering students, and personal preferences.

**Chunking & Indexing Strategy:**  
All documents are split into overlapping chunks of **220–280 words** with a **40-word overlap** so sentences and context are not cut abruptly across boundaries. Each chunk stores `source` (filename) and `chunk_id` metadata. Dense embeddings are precomputed once and saved as `embeddings.npy` so app startup remains fast on cloud CPU instances.

---

## 2. Hybrid Retrieval & Fusion Method

For every user query, the retrieval pipeline executes two independent searches and merges them:

1. **BM25 Keyword Search:** Scores exact lexical token overlap, excelling on rare technical identifiers, cryptographic standards, and project names.
2. **Dense Semantic Search:** Computes cosine similarity between the query embedding and precomputed chunk embeddings in `embeddings.npy`, capturing paraphrases and conceptual similarity even when exact keywords do not match.
3. **Reciprocal Rank Fusion (RRF):** Combines both ranked lists into a single unified ranking using:

$$\text{RRF}(d) = \sum_{r \in \{\text{BM25},\, \text{Dense}\}} \frac{1}{60 + \text{rank}_r(d)}$$

**Alternative Fusion Method Considered:**  
An alternative hybrid approach is a **min-max normalized weighted linear score**:

$$\text{Score}(d) = \alpha \cdot \text{Norm}(\text{Dense}(d)) + (1 - \alpha) \cdot \text{Norm}(\text{BM25}(d))$$

RRF was chosen over weighted linear scoring because raw BM25 scores are unbounded while cosine similarities lie in $[-1, 1]$; rank-based fusion avoids sensitivity to outlier score spikes without requiring hyperparameter tuning of $\alpha$.

---

## 3. Retrieval Evaluation (5 Test Questions)

| Question | BM25 result | Dense result | Hybrid result | Best mode and why |
| :--- | :--- | :--- | :--- | :--- |
| **Q1 (Exact rare keyword):** What encryption algorithms did you implement in File Vault? | Ranked `07_faqs.md` (Chunk #4, Q26) #1 with high exact-term match on `File Vault`, `AES-256-GCM`, and `RSA-2048 OAEP`. | Ranked `05_software_projects.md` #1 and `07_faqs.md` (Chunk #4) #2; captured cryptography concepts cleanly. | Ranked `07_faqs.md` (Chunk #4) #1 (`RRF: 0.0328`) and `05_software_projects.md` #2 (`RRF: 0.0320`). | **BM25 / Hybrid** — Rare exact cryptographic identifiers (`AES-256-GCM`, `OAEP`) gave BM25 top precision, which Hybrid retained at rank #1 while adding project context. |
| **Q2 (Paraphrased, zero shared words):** How do you make sweet treats and baked goods in your kitchen? | Missed primary dessert passages (0 overlap with *"sweet treats"*, *"baked goods"*, *"kitchen"*); returned low-relevance chunks. | Ranked `06_personality_hobbies_and_culinary.md` #1 and `07_faqs.md` (Chunk #4, Q27) #2 via semantic match to *"dessert"*, *"Tiramisu"*, and *"mascarpone"*. | Promoted `06_personality_hobbies_and_culinary.md` to #1 (`RRF: 0.0164`) via Dense rank contribution. | **Dense (and Hybrid)** — Because the query shared zero keywords with the source text, BM25 failed completely while Dense embeddings matched the culinary meaning. |
| **Q3 (Technical project overview):** Tell me about your final year project Emora. | Ranked `03_emora_fyp.md` (Chunk #0) #1 via exact match on `"Emora"`. | Ranked `03_emora_fyp.md` (Chunk #0) #1 and multimodal architecture (Chunk #2) #2. | Ranked `03_emora_fyp.md` (Chunk #0) #1 (`RRF: 0.0328`) and Chunk #2 #2 (`RRF: 0.0320`). | **Hybrid** — Combines exact project-name retrieval with semantically related multimodal fusion and Grad-CAM chunks. |
| **Q4 (Personal taste & media):** Do you watch any movies? | Ranked `07_faqs.md` (Chunk #2, Q12) #1 via exact match on `"movies"`. | Ranked `07_faqs.md` (Chunk #2, Q12) #1 and `06_personality_hobbies_and_culinary.md` (Studio Ghibli section) #2. | Ranked `07_faqs.md` (Chunk #2, Q12) #1 (`RRF: 0.0328`) and Studio Ghibli notes #2. | **Hybrid** — Surfaces both the direct FAQ answer (*Turbo*, Pixar) and extended Studio Ghibli favorites (*When Marnie Was There*, *The Wind Rises*). |
| **Q5 (Study habits & advice):** What advice would you give a junior software engineering student? | Ranked `07_faqs.md` (Chunk #4, Q24) #1 via exact match on `"junior"` and `"student"`. | Ranked `07_faqs.md` (Chunk #4, Q24) #1 and exam-prep workflow (Q25) #2. | Ranked `07_faqs.md` (Chunk #4, Q24) #1 (`RRF: 0.0328`) and `02_technical_stack_and_workflows.md` #2. | **Hybrid** — Pairs exact lexical matching on `"junior student"` with semantically related study and Git workflow notes. |

---

## 4. Failure Case Analysis

- **Test Query:** *"What exact learning rates and random seeds did you run during your Emora model experiments?"*
- **Observed Behavior:** The clone replied with a general overview of the Emora vision and text backbones (ResNet-50, DenseNet-121, ViT, RoBERTa) or stated *"I don't have that in my notes,"* rather than listing the exact hyperparameter grid (`1e-5` to `3e-4` and seeds `42, 13, 2024`).
- **Root Cause Explanation:** Two factors caused this weak response:
  1. **Knowledge Base Granularity:** `03_emora_fyp.md` documented the high-level architecture, dataset, and explainability methods, while granular hyperparameter sweep logs lived in separate training scripts outside `data/`. Because the system prompt strictly prohibits guessing beyond retrieved context, the LLM refused to invent numbers.
  2. **Top-$k$ Chunk Competition:** Broad project overview chunks had higher overall query overlap with `"Emora model experiments"` than lower-level implementation paragraphs, pushing specific training setup details outside the top-$k$ cutoff.

---

## 5. Future Improvement

- **Cross-Encoder Reranking & Conversational Memory:** Introduce a lightweight cross-encoder reranker (such as `cross-encoder/ms-marco-MiniLM-L-6-v2`) over the top-10 RRF candidates to score `(query, chunk)` pairs jointly before passing the top-3 chunks to Groq. Pairing this with short-term conversation memory would also allow multi-turn follow-up questions (e.g., *"How did you evaluate it?"*) to resolve references accurately.

---

## Local Setup

1. **Clone the Repository & Install Dependencies**
   ```bash
   git clone [https://github.com/ZahraInTech/zahra-digital-clone.git](https://github.com/ZahraInTech/zahra-digital-clone.git)
   cd zahra-digital-clone
   pip install -r requirements.txt