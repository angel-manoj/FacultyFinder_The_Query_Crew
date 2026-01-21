Prompt 1 — Ingestion (Web Scraping)
Prompt:
You are a Data Engineer building a web scraping pipeline to extract faculty data from a university website.
The site contains multiple faculty cards on a listing page, each linking to an individual profile page.
Explain how to design a scraping workflow using Python, requests, and BeautifulSoup that reliably navigates the directory, fetches individual profile pages, and handles issues like pagination or missing profile links.

Tool Used: ChatGPT 
Response:
Received guidance on structuring a two-step scraping process:
Scrape faculty listing cards
Visit individual profile pages for detailed data
Learned to use requests with headers and BeautifulSoup.
Added delays between requests to avoid server blocking.

Issues Faced & Resolution:
Some faculty cards had missing profile links - added null checks before visiting pages.
Website structure varied slightly across profiles - handled with conditional selectors.

Prompt 2 — Transformation 
Prompt:
I have scraped raw HTML content from faculty profile pages, including bios, teaching details, and research interests.
Many fields contain HTML tags, special characters, inconsistent spacing, or missing values.
As a Data Engineer, explain best practices for cleaning and normalizing this data using pandas, including handling null bios and preparing the text for downstream NLP tasks.

Solution:
Used conditional checks to handle missing fields.
Ensured consistent column structure before saving data.

Prompt 3 — FastAPI 
Prompt:
I am building a FastAPI service that exposes cleaned faculty data stored in SQLite.
The API should allow a Data Scientist to fetch all faculty records as JSON so they can generate embeddings and perform semantic search.
Explain how to structure the FastAPI application with clear separation between database logic and API routes, and how to handle cases where the database or website data is unavailable.
Solution:
Designed a FastAPI structure separating DB logic from API routes.
Implemented endpoints to return faculty data as JSON.
Used SQLite for persistent storage.
Issues Faced & Resolution:
API failed when database was unavailable - added try-except blocks and proper error responses.
Initial response size was large - optimized queries to return only required fields.

