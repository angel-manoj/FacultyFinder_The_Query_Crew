"""
build_embeddings.py

Generate MPNet sentence embeddings.
"""

import json
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent
ARTIFACT_DIR = BASE_DIR / "model" / "artifacts"

DATA_PATH = ARTIFACT_DIR / "faculty_data.json"
EMBED_PATH = ARTIFACT_DIR / "faculty_embeddings.npy"
META_PATH = ARTIFACT_DIR / "faculty_meta.json"

MODEL_NAME = "all-mpnet-base-v2"


def main():
    print("🔍 Loading faculty data...")
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    texts = [d["text"] for d in data]

    metadata = [
    {
        "id": d["id"],
        "name": d["name"],
        "email": d["email"],
        "specialization": d["specialization"],
        "phone": d.get("phone"), 
        "research_areas": d["research_areas"],
        "bio": d["bio"],
        "education": d["education"],
        "profile": d.get("profile"),
        "text": d["text"]
        }
        for d in data
    ]


    print("🧠 Loading model:", MODEL_NAME)
    model = SentenceTransformer(MODEL_NAME)

    embeddings = model.encode(
        texts,
        batch_size=16,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    np.save(EMBED_PATH, embeddings)

    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print("✅ Embeddings created:", embeddings.shape)


if __name__ == "__main__":
    main()
