# Faculty Finder – End‑to‑End Semantic Search System

A full‑stack **Big Data Engineering (BDE)** project that scrapes, processes, stores, and semantically searches university faculty data. The system combines a robust **data pipeline**, **SQLite-backed APIs**, **embedding-based semantic search**, and a **zero-build frontend UI**.

---

## Table of Contents

* [Overview](#overview)
* [System Architecture](#system-architecture)
* [Tech Stack](#tech-stack)
* [Data Schema](#data-schema)
* [Project Structure](#project-structure)
* [Pipeline Workflow](#pipeline-workflow)
* [Semantic Search & Recommender](#semantic-search--recommender)
* [API Usage](#api-usage)
* [Frontend](#frontend)
* [Installation & Setup](#installation--setup)
* [Data Statistics](#data-statistics)
* [Help & Troubleshooting](#help--troubleshooting)
* [Contributors](#contributors)

---

## Overview

**Faculty Finder** is an end-to-end faculty discovery platform designed to help users find academic experts using **semantic search** rather than keyword matching.

🚀 **Live Demo (Hosted on Railway)**
👉 [https://faculty-finder-production-507e.up.railway.app/](https://faculty-finder-production-507e.up.railway.app/)

Basic Idea & Workflow
At a high level, Faculty Finder follows a simple but powerful idea: ingest raw faculty data, enrich it using semantic embeddings, and make it easily searchable through APIs and a user-friendly interface.

The project workflow is:

* Recreate a reproducible Python environment
* Scrape and ingest faculty profiles from institutional websites
* Clean and transform raw HTML/JSON data into structured CSV and SQLite formats
* Store structured faculty data in a SQLite database
* Build vector embeddings for faculty profiles to enable semantic retrieval
* Apply a recommender pipeline to rerank results based on semantic relevance
* Expose faculty data and semantic search via FastAPI REST endpoints
* Serve ranked results through a lightweight, publicly hosted frontend UI
---

## System Architecture

```
Web Sources
     ↓
Scraper (scraper.py)
     ↓
Transform & Clean (transform.py)
     ↓
SQLite Storage (db_setup.py)
     ↓
Embedding Builder (build_embeddings.py)
     ↓
Semantic Search + Reranking (recommender.py)
     ↓
FastAPI Backend (main.py / semantic_api.py)
     ↓
Frontend UI (HTML + CSS + JS)
```

---

## Tech Stack

### Backend & Data

* Python 3.8+
* FastAPI
* SQLite
* Pandas
* Sentence Transformers (for embeddings)

### Frontend

* HTML5
* TailwindCSS (CDN)
* Vanilla JavaScript
* Zero build / no bundler

### Analysis

* Jupyter Notebook (`eda.ipynb`)

---

## Data Schema

### Core Fields

| Column            | Description              |
| ----------------- | ------------------------ |
| name              | Faculty full name        |
| profile           | Profile URL              |
| education         | Academic background      |
| phone             | Contact number           |
| address           | Office address           |
| email             | Email ID                 |
| specialization    | Areas of expertise       |
| personal_links    | Scholar / personal links |
| bio               | Professional biography   |
| teaching          | Courses taught           |
| research_areas    | Research interests       |
| journal_articles  | Journal publications     |
| conference_papers | Conference publications  |

### SQLite Table

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
FacultyFinder/
├── main.py                 # FastAPI entry point
├── semantic_api.py         # Semantic search endpoints
├── recommender.py          # Embedding similarity + reranking
├── build_embeddings.py     # Vector embedding builder
├── pipeline.py             # End-to-end pipeline runner
├── fetch_data.py           # Data loading helpers
├── scraper.py              # Web scraping logic
├── transform.py            # Data cleaning & transformation
├── db_setup.py             # SQLite schema & insertion
├── eda.ipynb               # Data analysis notebook
│
├── index.html              # Frontend UI
├── styles.css              # UI styles
├── script.js               # UI logic
│
├── data/
│   ├── raw_data.json
│   └── raw_data.csv
│
├── embeddings/
│   └── faculty_embeddings.pkl
│
└── README.md
```

---

## Pipeline Workflow

### 1. Scraping

* Extracts faculty details from institutional web pages
* Handles inconsistent HTML layouts

### 2. Transformation

* Cleans text fields
* Normalizes lists and missing values
* Outputs CSV and JSON

### 3. Storage

* Inserts cleaned data into SQLite
* Enables fast structured querying

### 4. Embedding Generation

* Builds dense vector representations for faculty profiles
* Stores embeddings for semantic similarity search

---

## Semantic Search & Recommender

* Uses **sentence-level embeddings** for semantic matching
* Computes cosine similarity between query and faculty profiles
* Applies reranking to surface the most relevant faculty
* Returns ranked results with relevance scores

This allows users to search using **natural language queries** such as:

> "machine learning in healthcare"

---

## API Usage

### Start Server

```bash
uvicorn main:app --reload --port 8000
```

### Example Endpoints

| Method | Endpoint         | Description             |
| ------ | ---------------- | ----------------------- |
| GET    | /faculty         | List all faculty        |
| GET    | /faculty/search  | Search by name or ID    |
| POST   | /semantic-search | Semantic faculty search |

---

## Frontend

The frontend is a **zero-build UI**:

* Open `index.html` directly in the browser
* Connects to FastAPI backend
* Supports:

  * Semantic search
  * Light / Dark mode
  * Relevance badges
  * Loading states
  * Responsive layout

---

## Installation & Setup

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate
pip install -r requirements.txt
```

### Run Full Pipeline (Recommended)

```bash
python pipeline.py --all
```

This command:

* Scrapes / loads raw data
* Cleans and transforms it
* Loads it into SQLite
* Builds embeddings for semantic search

### Run Backend API

```bash
uvicorn main:app --reload --port 8000
```

---

## Data Statistics

Derived from `eda.ipynb`:

* **Total faculty records**: 111
* **Total attributes per faculty**: 15
* **Unique specializations identified**: ~380+
* **Dominant research areas**:

  * Machine Learning
  * Computer Vision
  * Natural Language Processing
  * Information Retrieval

### Publication Insights

* **Average publications per faculty**: ~3
* **Publication range**: 0 to 60+

### Data Quality Notes

* Academic fields (name, teaching, specialization) are largely complete
* Contact details (phone, address, personal links) show higher missing rates
* Text-heavy fields show high variability, making them suitable for semantic embeddings

---

## Help & Troubleshooting

**Port already in use**

```bash
lsof -i :8000
kill -9 <PID>
```

**No semantic results returned**

* Ensure embeddings are built using `python pipeline.py --all`
* Check that embedding artifacts exist

**Frontend not showing results**

* Confirm backend is running
* Verify API URL in `script.js`

---

## Future Improvements

* Add Dockerfile and docker-compose for one-command deployment
* Add unit tests for pipeline and recommender components
* Expose OpenAPI / Swagger documentation for semantic endpoints
* Support incremental embedding updates for new faculty data

---

## Contributors

* **Deep Patel**
* **Angel Manoj**

---

© 2026 – Faculty Finder | The Query Crew
