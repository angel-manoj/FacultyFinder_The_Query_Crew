"""FastAPI service exposing DA-IICT faculty records from SQLite.

Provides endpoints to list all faculty and to search by `id` or `name`.
"""

from fastapi import FastAPI, Query
import sqlite3
from typing import Optional

app = FastAPI()

def get_db():
    """Open and return a SQLite connection to the `faculty.db` file.

    The returned connection uses `sqlite3.Row` as the row factory so
    rows can be converted directly into dict-like objects.

    Returns:
        sqlite3.Connection: an open SQLite connection.
    """
    conn = sqlite3.connect("faculty.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/faculty")
def get_all_faculty():
    """Return all rows from the `faculty` table as a list of dicts.

    Connects to the local SQLite database, queries the `faculty`
    table and returns the results in a JSON-serializable format.

    Returns:
        list[dict]: all faculty records.
    """
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
    """Search the `faculty` table by `id` and/or partial `name`.

    Both parameters are optional; when provided they are combined with
    an AND in the WHERE clause. The `name` parameter performs a
    case-insensitive LIKE match for convenience.

    Args:
        id (int | None): faculty `id` to match exactly.
        name (str | None): substring to match against `name`.

    Returns:
        list[dict]: matching faculty records.
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
