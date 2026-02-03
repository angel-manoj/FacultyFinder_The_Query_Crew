import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from vector_search.vector_store import create_faiss_index
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "faculty_clean.csv"
EMBED_PATH = BASE_DIR / "data" / "faculty_embeddings.npy"
INDEX_PATH = BASE_DIR / "data" / "faculty_faiss.index"

MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"

print("📄 Loading faculty data...")
df = pd.read_csv(DATA_PATH)

print("📦 Loading embeddings...")
embeddings = np.load(EMBED_PATH)

print("🧠 Loading model (local cache only)...")
model = SentenceTransformer(
    MODEL_NAME,
    local_files_only=True
)

# ---- FAISS INDEX (COSINE SIMILARITY) ----
if INDEX_PATH.exists():
    print("📦 Loading FAISS index from disk...")
    index = faiss.read_index(str(INDEX_PATH))
else:
    print("⚡ Building FAISS index (cosine similarity)...")
    index = create_faiss_index(embeddings)
    faiss.write_index(index, str(INDEX_PATH))

def search_faculty(query: str, top_k: int = 5):
    query_vec = model.encode([query])

    # Normalize query vector for cosine similarity
    query_vec = query_vec / np.linalg.norm(query_vec, axis=1, keepdims=True)

    scores, indices = index.search(query_vec, top_k)

    results = df.iloc[indices[0]].copy()
    results["score"] = scores[0]

    return results[
        ["name", "email", "specialization", "research_areas", "bio", "score"]
    ]

if __name__ == "__main__":
    print("🔍 Running test query...")
    res = search_faculty("sustainable energy and carbon capture")
    print(res)
