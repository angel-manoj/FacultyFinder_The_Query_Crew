"""
FastAPI service for DA-IICT Faculty Finder.

Features:
1. Keyword-based faculty access using SQLite
2. Semantic faculty search using MPNet embeddings + FAISS
"""
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import sqlite3
from typing import Optional
from pathlib import Path
import logging

app = FastAPI(
    title="Faculty Finder",
    description="Keyword + Semantic faculty discovery system",
    version="1.0"
)

# Serve frontend UI
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")


# -------------------- LOGGING --------------------

logging.basicConfig(level=logging.INFO)

# -------------------- CORS MIDDLEWARE --------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Restrict later if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- PATHS --------------------

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "faculty.db"

# -------------------- DATABASE UTILS --------------------

def get_db():
    """Open and return a SQLite connection to faculty.db"""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# -------------------- KEYWORD SEARCH (SQLITE) --------------------

@app.get("/faculty")
def get_all_faculty():
    """Return all faculty records."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM faculty")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


@app.get("/faculty/search")
def search_faculty_sql(
    id: Optional[int] = Query(None, description="Faculty ID"),
    name: Optional[str] = Query(None, description="Faculty name (partial match)"),
    query_str: Optional[str] = Query(None, description="Keyword search")
):
    """Keyword-based search using SQLite."""
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

    if query_str is not None:
        search_term = f"%{query_str}%"
        query += """
            AND (
                name LIKE ? OR
                specialization LIKE ? OR
                research_areas LIKE ? OR
                teaching LIKE ? OR
                bio LIKE ? OR
                profile LIKE ?
            )
        """
        params.extend([search_term] * 6)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# -------------------- SEMANTIC SEARCH --------------------

@app.get("/faculty/semantic-search")
def search_faculty_semantic(
    query_str: str = Query(..., description="Semantic search query")
):
    """
    Semantic faculty search using MPNet embeddings + FAISS.
    Falls back to keyword search if model fails.
    """
    try:
        from model.recommender import search_faculty
        return search_faculty(query_str, top_k=8)

    except Exception as e:
        logging.error(f"Semantic search failed: {e}")

        # Fallback to keyword search
        conn = get_db()
        cursor = conn.cursor()
        search_term = f"%{query_str}%"
        cursor.execute(
            """
            SELECT * FROM faculty WHERE (
                name LIKE ? OR
                specialization LIKE ? OR
                research_areas LIKE ? OR
                teaching LIKE ? OR
                bio LIKE ? OR
                profile LIKE ?
            )
            """,
            [search_term] * 6
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
