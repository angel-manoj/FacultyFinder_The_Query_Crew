import sqlite3
import json

DB_PATH = "./faculty.db"
JSON_PATH = "./data/raw_data.json"


def create_table():
    """Create the `faculty` table in the SQLite database if missing.

    The schema mirrors the pipeline's JSON fields and stores list-like
    columns as strings to keep the DB simple and portable.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS faculty (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        profile TEXT,
        education TEXT,
        phone TEXT,
        address TEXT,
        email TEXT,
        specialization TEXT,
        personal_links TEXT,
        bio TEXT,
        teaching TEXT,
        research_areas TEXT,
        journal_articles TEXT,
        conference_papers TEXT
    )
    """)

    conn.commit()
    conn.close()
    print("Faculty table ready")


def load_json_to_db():
    """Load cleaned JSON records from `JSON_PATH` into SQLite.

    Each record is inserted as a single row; list-like fields are
    converted to strings to preserve content while storing in SQLite.
    """
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for row in data:
        cursor.execute("""
        INSERT INTO faculty (
            name, profile, education, phone, address, email,
            specialization, personal_links, bio, teaching,
            research_areas, journal_articles, conference_papers
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row.get("name"),
            row.get("profile"),
            row.get("education"),
            row.get("phone"),
            row.get("address"),
            row.get("email"),
            str(row.get("specialization")),
            row.get("personal_links"),
            row.get("bio"),
            str(row.get("teaching")),
            row.get("research_areas"),
            str(row.get("journal_articles")),
            str(row.get("conference_papers"))
        ))

    conn.commit()
    conn.close()
    print("JSON data inserted into SQLite")


def verify_count():
    """Print a simple row-count verification for the `faculty` table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM faculty")
    count = cursor.fetchone()[0]

    conn.close()
    print(f"Total rows in faculty table: {count}")


def run_db_pipeline():
    """Run the full DB preparation pipeline: create table, load JSON, verify."""
    create_table()
    load_json_to_db()
    verify_count()


if __name__ == "__main__":
    run_db_pipeline()
