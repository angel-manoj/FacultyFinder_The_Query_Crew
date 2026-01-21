from fastapi import FastAPI
import sqlite3

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

    data = [dict(row) for row in rows]

    conn.close()
    return data