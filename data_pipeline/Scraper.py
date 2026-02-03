"""
Web scraper utilities for DA-IICT faculty pages.

- Scrapes all faculty categories
- Extracts profile-level details
- Handles multiple publication layouts
- Stores ALL publications in a single `publications` column
- Safe for missing / inconsistent HTML
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


# -------------------------------------------------------------------
# CONFIG
# -------------------------------------------------------------------

URLS = [
    "https://www.daiict.ac.in/faculty",
    "https://www.daiict.ac.in/adjunct-faculty",
    "https://www.daiict.ac.in/adjunct-faculty-international",
    "https://www.daiict.ac.in/distinguished-professor",
    "https://www.daiict.ac.in/professor-practice"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9"
}

REQUEST_DELAY = 0.7


# -------------------------------------------------------------------
# HELPERS
# -------------------------------------------------------------------

def fetch(url):
    """Fetch HTML content safely."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print(f"[FETCH ERROR] {url} -> {e}")
        return None


def clean_text(tag):
    """Extract clean visible text from a BS tag."""
    return tag.get_text(" ", strip=True).replace("\xa0", " ") if tag else None


# -------------------------------------------------------------------
# SECTION EXTRACTORS
# -------------------------------------------------------------------

def extract_teaching(soup):
    """Extract teaching / courses."""
    teaching = []

    for li in soup.select("div.work-exp ul li"):
        txt = clean_text(li)
        if txt:
            teaching.append(txt)

    if not teaching:
        for p in soup.select("div.work-exp p"):
            if not p.find("a"):
                txt = clean_text(p)
                if txt:
                    teaching.append(txt)

    return teaching or None


def extract_research_areas(soup):
    """Extract research areas."""
    areas = []

    for li in soup.select("div.work-exp1 li"):
        txt = clean_text(li)
        if txt:
            areas.append(txt)

    if not areas:
        for p in soup.select("div.work-exp1 p"):
            txt = clean_text(p)
            if txt:
                areas.append(txt)

    return areas or None


def extract_publications(soup):
    """
    Extract ALL publications (journals + conferences + books).

    Handles:
    - Old pages (with h4 + ul)
    - New pages (multiple div.education blocks)
    """

    publications = set()

    # NEW / MOST COMMON LAYOUT
    for block in soup.select("div.education.overflowContent"):
        for li in block.select("ul li"):
            txt = clean_text(li)
            if txt:
                publications.add(txt)

    # OLD LAYOUT (fallback)
    if not publications:
        for ul in soup.select("div.education ul"):
            for li in ul.select("li"):
                txt = clean_text(li)
                if txt:
                    publications.add(txt)

    return list(publications) or None


# -------------------------------------------------------------------
# PROFILE SCRAPER
# -------------------------------------------------------------------

def extract_profile(profile_url):
    """Extract data from an individual faculty profile page."""

    html = fetch(profile_url)
    if not html:
        return None, None, None, None, None

    soup = BeautifulSoup(html, "html.parser")

    bio = clean_text(soup.select_one("div.about p"))
    teaching = extract_teaching(soup)
    research_areas = extract_research_areas(soup)

    link_tag = soup.select_one("div.field--name-field-sites a")
    personal_links = link_tag["href"] if link_tag else None

    publications = extract_publications(soup)

    return bio, teaching, research_areas, personal_links, publications


# -------------------------------------------------------------------
# FACULTY LISTING SCRAPER
# -------------------------------------------------------------------

def scrape(url):
    """Scrape one faculty listing page."""
    html = fetch(url)
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    cards = soup.find_all("div", class_="facultyDetails")

    print(f"Scraping {url} | Faculty found: {len(cards)}")

    rows = []

    for card in cards:
        try:
            name_tag = card.select_one("h3 a")
            name = clean_text(name_tag)
            profile = name_tag["href"] if name_tag else None

            education = clean_text(card.select_one(".facultyEducation"))
            phone = clean_text(card.select_one(".facultyNumber"))
            address = clean_text(card.select_one(".facultyAddress"))
            email = clean_text(card.select_one(".facultyemail"))
            specialization = clean_text(card.select_one(".areaSpecialization p"))

            bio, teaching, research_areas, personal_links, publications = (
                extract_profile(profile) if profile else (None, None, None, None, None)
            )

            rows.append({
                "name": name,
                "profile": profile,
                "education": education,
                "phone": phone,
                "address": address,
                "email": email,
                "specialization": specialization,
                "personal_links": personal_links,
                "bio": bio,
                "teaching": teaching,
                "research_areas": research_areas,
                "publications": publications
            })

            time.sleep(REQUEST_DELAY)

        except Exception as e:
            print(f"[PARSE ERROR] {name if name else 'Unknown'} -> {e}")

    return rows


def run_scraper(output_path="data/raw_data.csv"):
    """Run scraper for all configured URLs."""
    all_data = []

    for url in URLS:
        print(f"\n▶ Scraping URL: {url}")
        all_data.extend(scrape(url))

    df = pd.DataFrame(all_data)
    df.to_csv(output_path, index=False)

    print(f"\n Scraping complete. Data saved to: {output_path}")
    print(f"Total faculty records: {len(df)}")


if __name__ == "__main__":
    run_scraper()
