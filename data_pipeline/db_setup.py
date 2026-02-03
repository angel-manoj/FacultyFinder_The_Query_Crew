import sqlite3
import json

DB_PATH = "./faculty.db"
JSON_PATH = "./data/clean_faculty_data.json"


def create_table():
    """
    Create the `faculty` table with the updated schema.
    List-like fields are stored as JSON-encoded TEXT.
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
        publications TEXT,
        embedding_text TEXT
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Faculty table ready (updated schema)")


def load_json_to_db():
    """
    Load cleaned JSON records into SQLite.
    All list/dict fields are serialized using json.dumps().
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
            research_areas, publications, embedding_text
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row.get("name"),
            row.get("profile"),
            row.get("education"),
            row.get("phone"),
            row.get("address"),
            row.get("email"),

            # ✅ Serialize list-like fields
            json.dumps(row.get("specialization", [])),
            json.dumps(row.get("personal_links", [])),
            row.get("bio"),
            json.dumps(row.get("teaching", [])),
            json.dumps(row.get("research_areas", [])),
            json.dumps(row.get("publications", [])),

            row.get("embedding_text")
        ))

    conn.commit()
    conn.close()
    print("✅ JSON data inserted into SQLite")


def verify_count():
    """Verify total rows in the faculty table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM faculty")
    count = cursor.fetchone()[0]

    conn.close()
    print(f"📊 Total rows in faculty table: {count}")


def run_db_pipeline():
    """Run full DB pipeline."""
    create_table()
    load_json_to_db()
    verify_count()


if __name__ == "__main__":
    run_db_pipeline()
