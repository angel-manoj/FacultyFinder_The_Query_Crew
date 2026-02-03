"""
FastAPI service for DA-IICT Faculty Finder.

Features:
1. Keyword-based faculty access using SQLite
2. Semantic faculty search using MPNet embeddings + FAISS
"""

from fastapi import FastAPI, Query
import sqlite3
from typing import Optional
from vector_search.search import search_faculty as semantic_search

# -------------------- APP SETUP --------------------

app = FastAPI(
    title="Faculty Finder",
    description="Keyword + Semantic faculty discovery system",
    version="1.0"
)

# -------------------- DATABASE UTILS --------------------

def get_db():
    """Open and return a SQLite connection to faculty.db"""
    conn = sqlite3.connect("faculty.db")
    conn.row_factory = sqlite3.Row
    return conn

# -------------------- KEYWORD SEARCH (SQLITE) --------------------

@app.get("/faculty")
def get_all_faculty():
    """
    Return all faculty records (keyword-based).
    """
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM faculty")
    rows = cursor.fetchall()

    conn.close()
    return [dict(row) for row in rows]


@app.get("/faculty/search")
def search_faculty_sql(
    id: Optional[int] = Query(None, description="Faculty ID"),
    name: Optional[str] = Query(None, description="Faculty name (partial match)")
):
    """
    Keyword-based search on faculty table using SQLite.
    """
    conn = get_db()
    cursor = conn.cursor()

    query = "SELECT * FROM faculty WHERE 1=1"
    params = []

    if id is not None:
        query += " AND id = ?"
        params.append(id)

    if name is not None:
        query += " AND name LIKE ?"
        params.append(f"%{name}%")

    cursor.execute(query, params)
    rows = cursor.fetchall()

    conn.close()
    return [dict(row) for row in rows]

# -------------------- SEMANTIC SEARCH (FAISS + MPNet) --------------------

@app.get("/search")
def semantic_search_api(
    query: str = Query(..., description="Natural language query"),
    top_k: int = Query(5, description="Number of results")
):
    """
    Semantic faculty search using transformer embeddings + FAISS.
    """
    results = semantic_search(query, top_k)
    return results.to_dict(orient="records")

# -------------------- HEALTH CHECK --------------------

@app.get("/")
def health():
    return {"status": "Faculty Finder is running"}
