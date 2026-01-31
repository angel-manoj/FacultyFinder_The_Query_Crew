"""Web scraper utilities for the DA-IICT faculty pages.

This module contains small helper functions to fetch HTML pages,
parse faculty cards and profile pages, and save the aggregated
results to `data/raw_data.csv` by default.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


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


def fetch(url):
    """Fetch the HTML content for a URL.

    Returns the response text on success or `None` on failure.
    """
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print("Fetch error:", e)
        return None


def extract_teaching(soup):
    """Extract a list of teaching/course strings from a profile soup.

    If no teaching entries are found the function returns the string
    "Not Provided" to match the rest of the pipeline's expectations.
    """
    teaching = []
    li_tags = soup.select("div.work-exp ul li")

    if li_tags:
        for li in li_tags:
            text = li.get_text(" ", strip=True).replace("\xa0", " ")
            if text:
                teaching.append(text)
    else:
        for p in soup.select("div.work-exp p"):
            if p.find("a"):
                continue
            text = p.get_text(" ", strip=True).replace("\xa0", " ")
            if text:
                teaching.append(text)

    return teaching if teaching else "Not Provided"

def extract_profile(profile_url):
    """Given a profile URL, fetch and extract profile fields.

    Returns a tuple: (bio, teaching, research_areas, personal_links, pubs_dict)
    where `pubs_dict` contains keys `journals` and `conferences` or `None`.
    """

    html = fetch(profile_url)
    if not html:
        return None, None, None, None, None

    soup = BeautifulSoup(html, "html.parser")

    bio_tag = soup.select_one("div.about p")
    bio = bio_tag.get_text(strip=True) if bio_tag else None

    teaching = extract_teaching(soup)

    research_areas = None
    li_tags = soup.select("div.work-exp1 li")
    p_tags = soup.select("div.work-exp1 p")

    if li_tags:
        research_areas = [li.get_text(strip=True) for li in li_tags]
    elif p_tags:
        research_areas = [p.get_text(strip=True) for p in p_tags]

    link_tag = soup.select_one("div.field--name-field-sites a")
    personal_links = link_tag["href"] if link_tag else None

    journals, conferences = [], []
    pub_block = soup.select_one("div.education.overflowContent")

    if pub_block:
        for h in pub_block.find_all("h4"):
            title = h.get_text(strip=True).lower()
            ul = h.find_next_sibling("ul")

            if not ul:
                continue

            papers = [
                li.get_text(" ", strip=True).replace("\xa0", " ")
                for li in ul.find_all("li")
            ]

            if "journal" in title:
                journals = papers
            elif "conference" in title:
                conferences = papers

    return bio, teaching, research_areas, personal_links, {
        "journals": journals or None,
        "conferences": conferences or None
    }


def scrape(url):
    """Scrape a faculty listing page and return a list of records.

    Each record is a dict matching the pipeline schema. If the page
    cannot be fetched an empty list is returned.
    """

    html = fetch(url)
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    cards = soup.find_all("div", class_="facultyDetails")

    print("Scraping page | Faculty count:", len(cards))
    data = []

    for card in cards:
        try:
            name_tag = card.select_one("h3 a")
            name = name_tag.get_text(strip=True)
            profile = name_tag["href"]

            education = card.select_one(".facultyEducation")
            education = education.get_text(strip=True) if education else None

            phone = card.select_one(".facultyNumber")
            phone = phone.get_text(strip=True) if phone else None

            address = card.select_one(".facultyAddress")
            address = address.get_text(strip=True) if address else None

            email = card.select_one(".facultyemail")
            email = email.get_text(strip=True) if email else None

            specialization = card.select_one(".areaSpecialization p")
            specialization = specialization.get_text(strip=True) if specialization else None

            bio, teaching, research_areas, personal_links, publications = extract_profile(profile)

            data.append({
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
                "journal_articles": publications["journals"] if publications else None,
                "conference_papers": publications["conferences"] if publications else None,
            })

            time.sleep(0.7)

        except Exception as e:
            print("Error parsing card:", e)

    return data

def run_scraper(output_path="data/raw_data.csv"):
    """Run the scraper over configured `URLS` and save results.

    Args:
        output_path (str): path to write the CSV file (default: `data/raw_data.csv`).
    """
    all_data = []

    for url in URLS:
        print(f"\nScraping URL: {url}")
        all_data.extend(scrape(url))

    df = pd.DataFrame(all_data)
    df.to_csv(output_path, index=False)
    print(f"\nAll faculty data saved to {output_path}")


if __name__ == "__main__":
    run_scraper()
