# Faculty Finder – End‑to‑End Semantic Search System

A full‑stack **Big Data Engineering (BDE)** project that scrapes, processes, stores, and semantically searches university faculty data. The system combines a robust **data pipeline**, **SQLite-backed APIs**, **embedding-based semantic search**, and a **zero-build frontend UI**.

---

## 📑 Table of Contents

* [Overview](#overview)
* [Why Semantic Search?](#why-semantic-search)
* [System Architecture](#system-architecture)
* [Tech Stack](#tech-stack)
* [Skills Demonstrated](#skills-demonstrated)
* [Data Schema](#data-schema)
* [Project Structure](#project-structure)
* [Pipeline Workflow](#pipeline-workflow)
* [Semantic Search & Recommender](#semantic-search-recommender)
* [Data Statistics](#data-statistics)
* [API Usage](#api-usage)
* [Frontend Features](#frontend-features)
* [Screenshots](#screenshots)
* [Installation & Setup](#installation-setup)
* [Help & Troubleshooting](#help-troubleshooting)
* [Contributors](#contributors)

---

## <a id="overview"></a>🚀 Overview

**Faculty Finder** is an end-to-end faculty discovery platform designed to help users find academic experts using **semantic search** rather than simple keyword matching.

🚀 **Live Demo (Hosted on Railway)**
👉 [https://faculty-finder-production-507e.up.railway.app/](https://faculty-finder-production-507e.up.railway.app/)

### Core Idea & Workflow
1. **Scrape & Ingest**: Extract raw faculty profiles from institutional websites.
2. **Clean & Transform**: Process HTML/JSON data into structured formats (CSV/SQLite).
3. **Store**: Persist structured data in a SQLite database.
4. **Embed**: Generate dense vector representations using MPNet for all profiles.
5. **Search & Rerank**: Use cosine similarity + cross-encoder reranking for precise retrieval.
6. **Deploy**: Serve results via FastAPI and a modern, responsive frontend.

---

## <a id="why-semantic-search"></a>💡 Why Semantic Search?

Standard keyword search fails when terminology differs. **Faculty Finder** understands the **underlying meaning** and context of your query, not just exact word matches, by using dense vector embeddings and high-precision re-ranking.

---

## <a id="system-architecture"></a>🏗️ System Architecture

```
[ Web Sources ] 
      ↓
[ Data Pipeline (Scraper.py -> transform.py -> db_setup.py) ]
      ↓
[ SQLite DB (faculty.db) ]
      ↓
[ Model Service (build_embeddings.py -> recommender.py) ]
      ↓
[ FastAPI Backend (main.py) ]
      ↓
[ Frontend UI (HTML/CSS/JS) ]
```

---

## <a id="tech-stack"></a>🛠️ Tech Stack

### Backend & Data
* **Python 3.13**
* **FastAPI**: High-performance web framework.
* **SQLite**: Lightweight relational database.
* **Pandas**: For data manipulation and EDA.
* **Sentence Transformers**: MPNet (all-mpnet-base-v2) for embeddings.
* **Cross-Encoder**: For high-precision reranking.

### Frontend
* **Vanilla HTML5 & CSS3**
* **TailwindCSS**: For modern styling.
* **Vanilla JavaScript**: For dynamic search and theme toggling.

---

## <a id="skills-demonstrated"></a>🧠 Skills Demonstrated

* **Data Engineering & ETL**: Automated multi-stage data pipelines.
* **Web Scraping**: Extracting structured data from messy institutional HTML.
* **Data Cleaning**: Handling nulls, normalizing fields, and statistical analysis.
* **Vector Embeddings**: Implementing state-of-the-art NLP models for retrieval.
* **Semantic Retrieval**: Cosine similarity and re-ranking architectures.
* **API Development**: Building robust RESTful services with FastAPI.
* **Full Stack Deployment**: Zero-build frontend integration with live hosting.

---

## <a id="data-schema"></a>📦 Data Schema

The SQLite database stores normalized faculty records. Core fields include:

| Column | Description |
| :--- | :--- |
| **name** | Faculty full name |
| **profile** | Original profile URL |
| **education**| Academic background |
| **phone** | Contact number |
| **address** | Office address |
| **email** | Email ID |
| **specialization** | Areas of expertise |
| **personal_links** | Scholar / personal links |
| **bio** | Professional biography |
| **teaching** | Courses taught |
| **research_areas** | Research interests |
| **publications** | List of publications |

### SQLite Table Structure
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
  publications TEXT
);
```

---

## <a id="project-structure"></a>📂 Project Structure

```bash
FacultyFinder/
├── main.py                 # FastAPI Main Entry Point
├── pipeline.py             # End-to-end Pipeline Runner
├── faculty.db              # SQLite Database
├── requirements.txt        # Project Dependencies
│
├── data_pipeline/          # Raw Data Processing
│   ├── Scraper.py          # Web scraping logic
│   ├── transform.py        # Data cleaning & CSV generation
│   ├── db_setup.py         # SQLite schema & insertion
│   └── eda.ipynb           # Data Science Analysis (Statistics)
│
├── model/                  # AI & Search Logic
│   ├── build_embeddings.py # Generates vector embeddings
│   ├── recommender.py      # Semantic search + Reranking logic
│   ├── artifacts/          # Saved embeddings & metadata
│   └── semantic_api.py     # Semantic-specific logic
│
├── frontend/               # UI Files
│   ├── index.html          
│   ├── styles.css          
│   └── script.js           
│
└── data/                   # Data Storage
    ├── raw_data.json       # Initial scraped output
    ├── clean_faculty_data.csv
    └── clean_faculty_data.json
```

---

## <a id="pipeline-workflow"></a>🔄 Pipeline Workflow

### 1. Scraping
Extracts faculty data from institutional web pages and handles inconsistent HTML layouts to ensure complete data ingestion.

### 2. Transformation
Cleans text fields, normalizes lists (e.g., teaching, publications), handles null values, and exports the data to structured CSV and JSON formats.

### 3. Storage
Loads the cleaned and structured data into a SQLite database (`faculty.db`) to enable fast, relational querying.

### 4. Embedding Generation
Creates dense vector representations using **MPNet** for all faculty profiles, enabling high-performance semantic similarity search.

---

## <a id="semantic-search-recommender"></a>🔍 Semantic Search & Recommender

* Uses **sentence-level embeddings** for semantic matching.
* Computes **cosine similarity** between user query and faculty profiles.
* Applies **cross-encoder reranking** to surface the most relevant faculty with high precision.
* Returns ranked results with relevance badges based on confidence scores.

---

## <a id="data-statistics"></a>📊 Data Statistics

Derived from comprehensive analysis in `data_pipeline/eda.ipynb`:

* **Total Faculty Records**: 112
* **Average Publications per Faculty**: 7.41 (Range: 0 - 50)
* **Education Quality**: 84.82% of faculty hold a **PhD**.
* **Data Availability**: 97.32% have teaching info; 16.96% have dedicated research area lists.

### Column-wise Data Quality (Null Analysis)

| Column | Null Count | Null Percentage |
| :--- | :--- | :--- |
| name | 0 | 0.00% |
| profile | 0 | 0.00% |
| education | 2 | 1.79% |
| phone | 34 | 30.36% |
| address | 35 | 31.25% |
| email | 1 | 0.89% |
| specialization | 0 | 0.00% |
| personal_links | 65 | 58.04% |
| bio | 43 | 38.39% |
| teaching | 3 | 2.68% |
| research_areas | 93 | 83.04% |
| publications | 44 | 39.29% |

---

## <a id="api-usage"></a>🔌 API Usage

### Start the Server
```bash
uvicorn main:app --reload --port 8000
```

### Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/` | Serves the Frontend UI |
| **GET** | `/faculty` | Get all faculty records |
| **GET** | `/faculty/search?query_str=...` | Keyword search across all fields |
| **GET** | `/faculty/semantic-search?query_str=...` | AI-powered semantic (embedding) search |

**Example Semantic Query:**
`GET /faculty/semantic-search?query_str=machine learning`

---

## <a id="frontend-features"></a>🖥️ Frontend Features

* **Hybrid Search**: Automatically defaults to semantic search with keyword fallback.
* **Modern UI**: Dark/Light mode support with smooth transitions.
* **Relevance Ranking**: Displays "Most Relevant" badges for high-confidence matches.
* **Responsive Design**: Optimized for both mobile and desktop views.

---

## <a id="screenshots"></a>📸 Screenshots
### Query 1 – Natural Language Processing
<img width="1894" height="1127" alt="Screenshot 2026-02-07 133833" src="https://github.com/user-attachments/assets/9d085bb7-668b-482c-b03b-26f96ec54925" />

### Query 2 – Computer Vision (Dark Mode)
<img width="1900" height="1125" alt="Screenshot 2026-02-07 133910" src="https://github.com/user-attachments/assets/98064fae-41f9-4a89-b0b4-debe22c18390" />

### Query 3 – No Matching Results
<img width="1888" height="1123" alt="Screenshot 2026-02-07 133939" src="https://github.com/user-attachments/assets/156ff77c-e225-4d24-8389-1c298888792a" />

---

## <a id="installation-setup"></a>⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/angel-manoj/FacultyFinder_The_Query_Crew.git
cd FacultyFinder_The_Query_Crew
```

### 2. Create Virtual Environment
```powershell
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Data (Step-by-Step)
If you need to regenerate the database and embeddings from scratch:
```bash
# Step 1: Run basic pipeline (Scrape -> Clean -> Store)
python pipeline.py --all

# Step 2: Build AI vector embeddings
python model/build_embeddings.py
```

---

## <a id="help-troubleshooting"></a>❓ Help & Troubleshooting

* **Port 8000 already in use**: 
  * Windows: `netstat -ano | findstr :8000` then `taskkill /F /PID <PID>`
* **ModuleNotFoundError**: Ensure your virtual environment is activated (`.\venv\Scripts\activate`).
* **API Error 404 on Search**: Always access the project via `http://localhost:8000` (FastAPI), not by opening the HTML file directly or via port 8001.

---

## <a id="contributors"></a>👥 Contributors

* **Angel Manoj**
* **Deep Patel**

---
© 2026 – Faculty Finder | The Query Crew

