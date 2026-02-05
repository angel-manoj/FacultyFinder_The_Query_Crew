"""
FastAPI service for DA-IICT Faculty Finder.

Features:
1. Keyword-based faculty access using SQLite
2. Semantic faculty search using MPNet embeddings + FAISS
3. Serves frontend UI
"""

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import sqlite3
from typing import Optional
from pathlib import Path
import logging

# -------------------- APP SETUP --------------------

app = FastAPI(
    title="Faculty Finder",
    description="Keyword + Semantic faculty discovery system",
    version="1.0"
)

# -------------------- LOGGING --------------------

logging.basicConfig(level=logging.INFO)

# -------------------- CORS --------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- PATHS --------------------

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "faculty.db"

# -------------------- DATABASE --------------------

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# -------------------- HEALTH CHECK --------------------

@app.get("/api")
def health_check():
    return {"status": "Faculty Finder API is live"}

# -------------------- GET ALL FACULTY --------------------

@app.get("/faculty")
def get_all_faculty():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM faculty")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# -------------------- KEYWORD SEARCH --------------------

@app.get("/faculty/search")
def search_faculty_sql(
    id: Optional[int] = Query(None),
    name: Optional[str] = Query(None),
    query_str: Optional[str] = Query(None)
):
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
def search_faculty_semantic(query_str: str):
    try:
        from model.recommender import search_faculty
        return search_faculty(query_str, top_k=8)

    except Exception as e:
        logging.error(f"Semantic search failed: {e}")

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

# -------------------- SERVE FRONTEND (IMPORTANT: LAST) --------------------

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
