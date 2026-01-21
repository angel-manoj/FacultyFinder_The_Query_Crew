import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# URL = "https://www.daiict.ac.in/faculty"
# URL= "https://www.daiict.ac.in/adjunct-faculty"
# URL="https://www.daiict.ac.in/adjunct-faculty-international"
URL = "https://www.daiict.ac.in/professor-practice"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9"
}

def fetch(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        return r.text
    except:
        return None

def extract_teaching(soup):

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

    if not teaching:
        return "Not Provided"

    return teaching


def extract_profile(profile_url):

    html = fetch(profile_url)
    if not html:
        return None, None, None, None, None

    soup = BeautifulSoup(html, "html.parser")

    bio_tag = soup.select_one("div.about p")
    bio = bio_tag.text.strip() if bio_tag else None

    teaching = extract_teaching(soup)

    research_areas = None

    li2 = soup.select("div.work-exp1 li")
    p_tags = soup.select("div.work-exp1 p")

    if li2:
        research_areas = [t.get_text(strip=True) for t in li2]
    elif p_tags:
        research_areas = [p.get_text(strip=True) for p in p_tags]

    link_tag = soup.select_one("div.field--name-field-sites a")
    personal_links = link_tag["href"] if link_tag else None

    journals = []
    conferences = []

    pub_block = soup.select_one("div.education.overflowContent")

    section_headers = []

    if pub_block:
        section_headers = pub_block.find_all("h4")

        for h in section_headers:
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

            if "conference" in title:
                conferences = papers

    return bio, teaching, research_areas, personal_links, {
        "journals": journals if journals else None,
        "conferences": conferences if conferences else None
    }


def scrape():

    html = fetch(URL)
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    cards = soup.find_all("div", class_="facultyDetails")

    print("Total faculty:", len(cards))
    data = []

    for card in cards:
        try:
            name_tag = card.select_one("h3 a")
            name = name_tag.text.strip()
            profile = name_tag["href"] 

            education = card.select_one(".facultyEducation")
            education = education.text.strip() if education else None

            phone = card.select_one(".facultyNumber")
            phone = phone.text.strip() if phone else None

            address = card.select_one(".facultyAddress")
            address = address.text.strip() if address else None

            email = card.select_one(".facultyemail")
            email = email.text.strip() if email else None

            specialization = card.select_one(".areaSpecialization p")
            specialization = specialization.text.strip() if specialization else None

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
            print("Error:", e)

    return data


df = pd.DataFrame(scrape())
df.to_csv("data/raw_data.csv", index=False)

print("Saved successfully!")
