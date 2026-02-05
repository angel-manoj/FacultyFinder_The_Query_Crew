"""
semantic_api.py

Lightweight semantic search helper (optional).
NOT used by main.py recommender route.
"""

import json
import logging
from pathlib import Path
from typing import List, Dict

import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder
from sklearn.metrics.pairwise import cosine_similarity

logging.basicConfig(level=logging.INFO)

BASE_DIR = Path(__file__).resolve().parent.parent
ARTIFACT_DIR = BASE_DIR / "model" / "artifacts"

EMBED_PATH = ARTIFACT_DIR / "faculty_embeddings.npy"
META_PATH = ARTIFACT_DIR / "faculty_meta.json"

EMBED_MODEL = "all-mpnet-base-v2"
RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

TOP_K = 5
CANDIDATES = 10

if not EMBED_PATH.exists() or not META_PATH.exists():
    raise FileNotFoundError("Embedding artifacts missing.")

_embeddings = np.load(EMBED_PATH)
with open(META_PATH, "r", encoding="utf-8") as f:
    _metadata: List[Dict] = json.load(f)

_embedder = SentenceTransformer(EMBED_MODEL)
_reranker = CrossEncoder(RERANK_MODEL)


def semantic_search(query: str) -> List[Dict]:
    query = query.lower().strip()

    query_vec = _embedder.encode([query], normalize_embeddings=True)
    scores = cosine_similarity(query_vec, _embeddings)[0]

    top_idx = np.argsort(scores)[::-1][:CANDIDATES]

    pairs = [(query, _metadata[i].get("text", "")) for i in top_idx]
    rerank_scores = _reranker.predict(pairs)

    ranked = sorted(
        zip(top_idx, rerank_scores),
        key=lambda x: x[1],
        reverse=True
    )

    results = []
    for idx, score in ranked[:TOP_K]:
        f = _metadata[idx]
        results.append({
            "name": f.get("name"),
            "email": f.get("email"),
            "phone": f.get("phone"),
            "education": f.get("education"),
            "bio": f.get("bio"),
            "profile": f.get("profile"),
            "rerank_score": float(score)
        })

    return results
