from fastapi import FastAPI, Query
import sqlite3
from typing import Optional

app = FastAPI()

def get_db():
    conn = sqlite3.connect("faculty.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/faculty")
def get_all_faculty():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM faculty")
    rows = cursor.fetchall()

    conn.close()
    return [dict(row) for row in rows]


@app.get("/faculty/search")
def search_faculty(
    id: Optional[int] = Query(None, description="Faculty ID"),
    name: Optional[str] = Query(None, description="Faculty name")
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

    cursor.execute(query, params)
    rows = cursor.fetchall()

    conn.close()
    return [dict(row) for row in rows]
