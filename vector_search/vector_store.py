import faiss
import numpy as np

def create_faiss_index(embeddings: np.ndarray):
    """
    Create a FAISS index using cosine similarity.

    Cosine similarity is implemented by:
    1. L2-normalizing embeddings
    2. Using inner product search (IndexFlatIP)
    """

    # Normalize embeddings
    faiss.normalize_L2(embeddings)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    print(f"✅ FAISS cosine index built with {index.ntotal} vectors")
    return index
