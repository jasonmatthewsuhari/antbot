# Search logic (Fish)

import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import os

# === Configurations ===
MODEL_NAME = "all-MiniLM-L6-v2"
OLLAMA_API = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"
EMBEDDINGS_FILE = "faq_embeddings.pkl"

# === Load Model and Embeddings Once ===
model = SentenceTransformer(MODEL_NAME)

if not os.path.exists(EMBEDDINGS_FILE):
    raise FileNotFoundError(f"❌ Embedding file '{EMBEDDINGS_FILE}' not found. Run embed.py first.")

with open(EMBEDDINGS_FILE, "rb") as f:
    data = pickle.load(f)
    questions = data["questions"]
    answers = data["answers"]
    embeddings = data["embeddings"]

# === Search Logic ===
def get_top_k_chunks(user_query: str, k: int = 3) -> str:
    query_emb = model.encode([user_query], convert_to_numpy=True)
    sims = cosine_similarity(query_emb, embeddings)[0]
    top_k_idxs = np.argsort(sims)[::-1][:k]

    chunks = [f"Q: {questions[i]}\nA: {answers[i]}" for i in top_k_idxs]
    return "\n\n".join(chunks)

# === Ollama Chat Logic ===
def query_ollama_with_context(user_input: str) -> str:
    context = get_top_k_chunks(user_input, k=3)
    prompt = f"""You are an assistant that only answers questions based on the FAQ provided.

FAQ:
{context}

User Question: {user_input}

Answer concisely based only on the FAQ above. If the answer cannot be found, say "I’m not sure based on the available information."
"""

    response = requests.post(OLLAMA_API, json={
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    })

    if not response.ok:
        return "❌ Failed to get response from Ollama."

    result = response.json()
    return result.get("response", "❌ No response content returned.")