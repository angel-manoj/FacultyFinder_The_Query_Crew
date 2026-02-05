"""
recommender.py

Hybrid faculty recommender system with:
- query intent normalization
- acronym expansion
- semantic embeddings (MPNet)
- entity / education boosting
- cross-encoder re-ranking
- soft entity cutoff
"""

import json
import math
import logging
from pathlib import Path
from typing import List, Dict

import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- LOGGING ----------------

logging.basicConfig(level=logging.INFO)

# ---------------- CONFIG ----------------

BASE_DIR = Path(__file__).resolve().parent.parent
ARTIFACT_DIR = BASE_DIR / "model" / "artifacts"

EMBED_PATH = ARTIFACT_DIR / "faculty_embeddings.npy"
META_PATH = ARTIFACT_DIR / "faculty_meta.json"

EMBED_MODEL = "all-mpnet-base-v2"
RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

TOP_K = 5
CANDIDATES = 10

# ---------------- SAFETY CHECK ----------------

if not EMBED_PATH.exists() or not META_PATH.exists():
    raise FileNotFoundError(
        "Embedding artifacts not found. "
        "Ensure faculty_embeddings.npy and faculty_meta.json "
        "exist before starting the API."
    )

# ---------------- GLOBAL MODEL CACHE ----------------

logging.info("Loading embedding and reranking models...")

_embedder = SentenceTransformer(EMBED_MODEL)
_reranker = CrossEncoder(RERANK_MODEL)
_embeddings = np.load(EMBED_PATH)

with open(META_PATH, "r", encoding="utf-8") as f:
    _metadata: List[Dict] = json.load(f)

logging.info("Models and artifacts loaded successfully")

# ---------------- QUERY NORMALIZATION ----------------

def normalize_query(query: str) -> str:
    query = query.lower()
    REMOVE_PHRASES = [
        "i want to do research in",
        "i want to do research",
        "i want to",
        "looking for",
        "interested in",
        "i am interested in",
        "can you suggest",
        "i want to work on",
        "i would like to work on"
    ]
    for phrase in REMOVE_PHRASES:
        query = query.replace(phrase, "")
    return " ".join(query.split())

# ---------------- ACRONYM EXPANSION ----------------

ACRONYM_MAP = {
    "ml": "machine learning",
    "dl": "deep learning",
    "ai": "artificial intelligence",
    "nlp": "natural language processing",
    "cv": "computer vision",
    "ir": "information retrieval",
    "hci": "human computer interaction",
    "iot": "internet of things",
    "dbms": "database management systems",
    "os": "operating systems",
    "ds": "data science",
    "nn": "neural networks",
    "rl": "reinforcement learning",
    "llm": "large language model"
}

def expand_acronyms(query: str) -> str:
    return " ".join(ACRONYM_MAP.get(w, w) for w in query.split())

# ---------------- QUERY TYPE DETECTION ----------------

def detect_query_type(query: str) -> str:
    words = query.split()
    if any(w in ACRONYM_MAP for w in words):
        return "topic"
    if len(words) >= 2:
        return "topic"
    return "entity"

# ---------------- ENTITY BOOST ----------------

def entity_boost(query: str, faculty: Dict) -> float:
    query = query.lower()
    score = 0.0

    education = str(faculty.get("education", "")).lower()
    bio = str(faculty.get("bio", "")).lower()
    text = str(faculty.get("text", "")).lower()

    if query in education:
        score += 0.40

    if query in bio:
        score += 0.15

    score += 0.02 * sum(1 for w in query.split() if w in text)
    return score

# ---------------- JSON SAFETY ----------------

def make_json_safe(obj):
    """
    Convert NaN / inf to None so FastAPI can serialize JSON safely.
    """
    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [make_json_safe(v) for v in obj]
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    return obj

# ---------------- SEARCH FUNCTION ----------------

def search_faculty(query: str, top_k: int = TOP_K) -> List[Dict]:
    normalized_query = normalize_query(query)
    expanded_query = expand_acronyms(normalized_query)

    query_type = detect_query_type(normalized_query)
    logging.info(f"Query type detected: {query_type}")

    semantic_query = f"{expanded_query} research faculty professor"

    query_vec = _embedder.encode(
        [semantic_query],
        normalize_embeddings=True
    )

    base_scores = cosine_similarity(query_vec, _embeddings)[0]

    hybrid_scores = []
    for i, faculty in enumerate(_metadata):
        score = base_scores[i]
        if query_type == "entity":
            score += entity_boost(normalized_query, faculty)
        hybrid_scores.append(score)

    candidate_idx = np.argsort(hybrid_scores)[::-1][:CANDIDATES]

    pairs = [
        (semantic_query, _metadata[i].get("text", ""))
        for i in candidate_idx
    ]

    rerank_scores = _reranker.predict(pairs)

    reranked = sorted(
        zip(candidate_idx, rerank_scores),
        key=lambda x: x[1],
        reverse=True
    )

    results = []
    for idx, score in reranked:
        faculty = _metadata[idx].copy()
        faculty["rerank_score"] = float(score)
        results.append(faculty)

    if query_type == "entity":
        results = [
            f for f in results
            if entity_boost(normalized_query, f) > 0
        ]

    return make_json_safe(results[:top_k])

# ---------------- CLI (LOCAL TESTING ONLY) ----------------

def main():
    print("🔍 Recommender ready (local mode)")
    print("-" * 50)

    while True:
        query = input("\nEnter research query (or exit): ").strip()
        if query.lower() == "exit":
            break

        results = search_faculty(query)

        print("\n🎓 Top matching faculty:\n")
        for i, f in enumerate(results, start=1):
            print(f"{i}. {f.get('name')}")
            print(f"   🎓 {f.get('education')}")
            print(f"   ⭐ Score: {f.get('rerank_score')}")
            print(f"   📝 {str(f.get('bio'))[:250]}...\n")

if __name__ == "__main__":
    main()
