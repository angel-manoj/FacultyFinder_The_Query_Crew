import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "faculty_clean.csv"
EMBED_PATH = BASE_DIR / "data" / "faculty_embeddings.npy"

MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"

def build_embeddings():
    print("📂 Project root:", BASE_DIR)
    print("📄 Loading data from:", DATA_PATH)

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"{DATA_PATH} not found")

    df = pd.read_csv(DATA_PATH)

    print("🧠 Loading embedding model:", MODEL_NAME)
    model = SentenceTransformer(
        MODEL_NAME,
        local_files_only=False  # first run requires internet
    )

    print("🔢 Generating embeddings for", len(df), "faculty...")
    embeddings = model.encode(
        df["embedding_text"].fillna("").tolist(),
        show_progress_bar=True
    )

    print("💾 Saving embeddings to:", EMBED_PATH)
    np.save(EMBED_PATH, embeddings)

    print("✅ MPNet embeddings successfully created!")

if __name__ == "__main__":
    build_embeddings()
