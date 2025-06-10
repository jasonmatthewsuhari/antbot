# Embedding logic (Fish)

from sentence_transformers import SentenceTransformer
import pickle
import re
import os

def generate_faq_embeddings(faq_path="data/faq.txt", output_path="faq_embeddings.pkl"):
    # 1: Read and parse faq.txt
    if not os.path.exists(faq_path):
        raise FileNotFoundError(f"❌ File not found: {faq_path}")
    
    with open(faq_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 2: Extract Q&A pairs
    qa_pairs = re.findall(r"Q:\s*(.*?)\nA:\s*(.*?)(?=\nQ:|\Z)", content, re.DOTALL)

    questions = [q.strip() for q, a in qa_pairs]
    answers = [a.strip() for q, a in qa_pairs]
    texts = [f"{q} {a}" for q, a in qa_pairs]  # For semantic meaning

    # 3: Load embedding model and generate embeddings
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(texts, convert_to_numpy=True)

    # 4: Save to pickle
    with open(output_path, "wb") as f:
        pickle.dump({
            "questions": questions,
            "answers": answers,
            "embeddings": embeddings
        }, f)

    print(f"✅ {len(qa_pairs)} embeddings saved to {output_path}")

if __name__ == "__main__":
    generate_faq_embeddings()
