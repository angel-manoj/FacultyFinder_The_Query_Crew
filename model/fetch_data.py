"""
fetch_data.py

Prepare model-ready faculty data from clean_faculty_data.csv
RUN LOCALLY ONLY.
"""

import json
import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "clean_faculty_data.csv"
OUTPUT_DIR = BASE_DIR / "model" / "artifacts"
OUTPUT_FILE = OUTPUT_DIR / "faculty_data.json"


def normalize_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    return " ".join(text.strip().split())


def safe_str(value) -> str:
    if pd.isna(value):
        return ""
    return str(value)


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError("clean_faculty_data.csv not found.")

    logging.info(f"Loading CSV: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)

    records = []
    for idx, row in df.iterrows():
        combined_text = f"""
        Research Areas: {safe_str(row.get('research_areas'))}
        Specialization: {safe_str(row.get('specialization'))}
        Bio: {safe_str(row.get('bio'))}
        Education: {safe_str(row.get('education'))}
        """

        text = normalize_text(combined_text)
        if not text:
            continue

        records.append({
            "id": idx,
            "name": safe_str(row.get("name")),
            "email": safe_str(row.get("email")),
            "phone": safe_str(row.get("phone")),
            "profile": safe_str(row.get("profile")),
            "image_url": safe_str(row.get("image_url")),
            "specialization": safe_str(row.get("specialization")),
            "research_areas": safe_str(row.get("research_areas")),
            "bio": safe_str(row.get("bio")),
            "education": safe_str(row.get("education")),
            "text": text
        })

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    logging.info(f"Saved {len(records)} faculty records")


if __name__ == "__main__":
    main()
