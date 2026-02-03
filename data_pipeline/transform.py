import pandas as pd
import re
import ast
import json


def run_transformation(
    input_csv="./data/raw_data.csv",
    output_csv="./data/clean_faculty_data.csv",
    output_json="./data/clean_faculty_data.json"
):
    """
    Load raw CSV, clean fields, and save cleaned data
    as both CSV (for EDA) and JSON (for downstream use).
    """

    # =========================
    # 1. LOAD DATA
    # =========================
    df = pd.read_csv(input_csv)

    # =========================
    # 2. BASIC CLEANING
    # =========================
    df.fillna({
        "phone": "Not Available",
        "email": "Not Available",
        "address": "Not Available",
        "specialization": "Not Available",
        "bio": "Not Provided",
        "teaching": "Not Provided",
        "personal_links": "Not Provided",
        "research_areas": "Not Provided",
        "publications": "[]"
    }, inplace=True)

    # Remove extra whitespace
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()

    # =========================
    # 3. EMAIL CLEANING
    # =========================
    def fix_email(email: str) -> str:
        email = email.replace("[at]", "@")
        email = email.replace("[dot]", ".")
        return email

    df["email"] = df["email"].apply(fix_email)

    # =========================
    # 4. NAME / ADDRESS CLEANING
    # =========================
    df["name"] = (
        df["name"]
        .str.replace(r"\(.*?\)", "", regex=True)
        .str.strip()
        .str.title()
    )

    df["address"] = df["address"].str.replace("#", "").str.strip()

    df["specialization"] = df["specialization"].str.replace(
        r"Meet\s+(Dr\.|Prof\.).*?:",
        "",
        regex=True
    )

    # =========================
    # 5. SPECIALIZATION → LIST
    # =========================
    def specialization_to_list(x):
        if pd.isna(x) or x == "Not Provided":
            return x
        return [i.strip() for i in str(x).split(",") if i.strip()]

    df["specialization"] = df["specialization"].apply(specialization_to_list)

    # =========================
    # 6. TEACHING CLEANING
    # =========================
    BLACKLIST = [
        "assistant", "assistant professor", "adjunct faculty",
        "teaching assistant", "professor", "role",
        "da-iict", "gandhinagar", "florida tech",
        "niser", "iit", "india", "usa"
    ]

    def clean_teaching_list(x):
        if pd.isna(x):
            return "Not Provided"

        x = str(x).strip("[]").replace("'", "")
        items = [i.strip() for i in x.split(",") if i.strip()]

        cleaned = []
        for item in items:
            item = item.replace("\xa0", " ").strip()
            item_lower = item.lower()

            if re.search(r"https?://|www\.", item):
                continue

            if any(b in item_lower for b in BLACKLIST):
                continue

            cleaned.append(item)

        return cleaned if cleaned else "Not Provided"

    df["teaching"] = df["teaching"].apply(clean_teaching_list)

    # =========================
    # 7. FIX PUBLICATIONS LIST
    # =========================
    def fix_list(x):
        if pd.isna(x):
            return []
        if isinstance(x, str):
            try:
                return ast.literal_eval(x)
            except Exception:
                return []
        if isinstance(x, list):
            return x
        return []

    df["publications"] = df["publications"].apply(fix_list)

    # =========================
    # 8. RESEARCH AREAS CLEANING
    # =========================
    def research_areas_list_to_string(x):
        if pd.isna(x) or str(x).strip() == "":
            return "Not Provided"

        if x == "Not Provided":
            return x

        if isinstance(x, str) and x.startswith("["):
            x = ast.literal_eval(x)

        if isinstance(x, list):
            return " ".join(x)

        return x

    df["research_areas"] = df["research_areas"].apply(
        research_areas_list_to_string
    )

    # =========================
    # 9. CREATE EMBEDDING COLUMN
    # =========================
    def build_embedding_text(row):
        parts = []

        if isinstance(row["specialization"], list):
            parts.append(" ".join(row["specialization"]))
        elif row["specialization"] not in ["Not Available", "Not Provided"]:
            parts.append(row["specialization"])

        if row["bio"] not in ["Not Available", "Not Provided"]:
            parts.append(row["bio"])

        if isinstance(row["teaching"], list):
            parts.append(" ".join(row["teaching"]))
        elif row["teaching"] not in ["Not Available", "Not Provided"]:
            parts.append(row["teaching"])

        if row["research_areas"] not in ["Not Available", "Not Provided"]:
            parts.append(row["research_areas"])

        return " ".join(parts).strip()

    df["embedding_text"] = df.apply(build_embedding_text, axis=1)

    # =========================
    # 10. SAVE CLEAN CSV (FOR EDA)
    # =========================
    df.to_csv(output_csv, index=False)
    print(f"Clean CSV saved → {output_csv}")

    # =========================
    # 11. SAVE JSON
    # =========================
    df.to_json(output_json, orient="records", indent=2)
    print(f"JSON saved → {output_json}")

    # =========================
    # 12. DEEP TEXT CLEANING (JSON)
    # =========================
    REPLACEMENTS = {
        r"\\xa0": " ",
        r"\\u2013": "",
        r"\\u201c": "",
        r"\\u201d": "",
        r"\\u2019": "'",

        "\xa0": " ",
        "\u2013": "",
        "\u201c": "",
        "\u201d": "",
        "\u2019": "'"
    }

    def clean_text(text: str) -> str:
        for k, v in REPLACEMENTS.items():
            text = re.sub(k, v, text)
        return re.sub(r"\s+", " ", text).strip()

    def deep_clean(obj):
        if isinstance(obj, str):
            return clean_text(obj)
        if isinstance(obj, list):
            return [deep_clean(i) for i in obj]
        if isinstance(obj, dict):
            return {k: deep_clean(v) for k, v in obj.items()}
        return obj

    with open(output_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    data = deep_clean(data)

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Cleaned JSON saved successfully!")


if __name__ == "__main__":
    run_transformation()
