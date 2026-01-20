# Big Data Engineering (BDE) - Faculty Finder Pipeline

A comprehensive data processing pipeline for faculty information extraction, transformation, and storage. This project processes faculty data from web sources and prepares it for NLP analysis.

## Table of Contents
- [Overview](#overview)
- [Data Schema](#data-schema)
- [Project Structure](#project-structure)
- [Pipeline Workflow](#pipeline-workflow)

---

## Overview

This project implements an end-to-end data engineering pipeline that:
1. **Scrapes** faculty information from institutional websites
2. **Transforms** raw data into structured formats (CSV, JSON)
3. **Cleans** data for NLP tasks.
4. **Stores** data in SQLite.
5. **Provides** API endpoints to query faculty data

### Technologies Used
- Python 3.8+
- FastAPI
- SQLite
- Pandas
- Jupyter Notebooks

---

## Data Schema

| Column Name          | Description |
|----------------------|-------------|
| `name`              | Faculty member’s full name |
| `profile`           | University profile link |
| `education`         | Educational background and degrees |
| `phone`             | Contact phone number |
| `address`           | Office address |
| `email`             | Email address |
| `specialization`    | Research specializations |
| `personal_links`    | Google Scholar, LinkedIn, or personal website links |
| `bio`               | Professional biography and experience |
| `teaching`          | Courses taught |
| `research_areas`    | Research areas and focus |
| `journal_articles`  | Published journal articles |
| `conference_papers` | Conference papers and presentations |


### JSON Format (`data/raw_data.json`)

```json
[
  {
    "name": "Faculty Name",
    "profile": "https://...",
    "education": "PhD in ...",
    "phone": "XXX-XXXX",
    "address": "...",
    "email": "email@...",
    "specialization": ["Area1", "Area2"],
    "personal_links": "https://...",
    "bio": "...",
    "teaching": ["Course1", "Course2"],
    "research_areas": ["Area1", "Area2"],
    "journal_articles": ["Article1", "Article2"],
    "conference_papers": ["Paper1", "Paper2"]
  }
]
```

### SQLite Database Schema

The SQLite database (`faculty.db`) contains a normalized schema:

```sql
CREATE TABLE faculty (
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
);

```

---

## Project Structure

```
BDE/
├── main.py                    # FastAPI server with endpoints
├── requirements.txt           # Python dependencies
├── README.md                  # Readme file
├── .gitignore                 # Git ignore rules
│
├── scripts/
│   ├── Scraper.py            # Web scraping module
│   └── Transformation.ipynb   # Data transformation notebook
│
├── data/
│   ├── raw_data.csv          # CSV format data
│   └── raw_data.json         # JSON format data
│
├── logs/
│   └── llm_usage.md          # LLM usage tracking
│
└── storage.ipynb             # Data storage and analysis notebook
```

---

## Pipeline Workflow

### 1. Data Scraping (`scripts/Scraper.py`)
- Extracts faculty information from institutional websites
- Handles HTML parsing and data extraction
- Validates and cleans raw data

### 2. Data Transformation (`scripts/Transformation.ipynb`)
- Converts raw data into structured formats
- Cleans text fields (removes special characters, standardizes formatting)
- Parses lists and arrays
- Handles missing values

### 3. Data Storage (`storage.ipynb`)
- Saves data to CSV format (`data/raw_data.csv`)
- Saves data to JSON format (`data/raw_data.json`)
- Creates SQLite database schema
- Inserts data into normalized database tables

### 4. Data Serving (`main.py`)
- FastAPI REST API for data access
- Query endpoints for faculty information
- JSON responses for easy integration

---

## Logging

LLM usage and processing logs are stored in:
- `logs/llm_usage.md` - Tracks LLM (Language Model) API usage

---
