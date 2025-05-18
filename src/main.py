from fastapi import FastAPI, Query, HTTPException
from urllib.parse import urlparse
from src.utils import Utils

import logging

from src.web_crawler import WebCrawler

# Configure basic logging
logging.basicConfig(level=logging.INFO)
app = FastAPI(title="Web Crawler API")

# Define an HTTP GET endpoint at /pages that starts the web crawling process
# Get the 'target' URL from the query string (e.g., /pages?target=https://example.com)
@app.get(
    "/pages",
    summary="Start crawling a website",
    description="Crawls all pages under the same domain starting from the given target URL."
)
def get_pages(target: str = Query(..., description="Full URL to start crawling from (e.g., https://example.com)")):

    crawler = WebCrawler()

    # Validate the target URL; return a 400 Bad Request error if invalid or missing
    if not target or not Utils.is_valid_url(target):
        raise HTTPException(status_code=400, detail="Invalid or missing URL")

    # Parse the URL to extract its domain
    parsed = urlparse(target)
    domain = parsed.netloc

    # Start crawling from the target URL, limited to the same domain
    crawler.crawl(target, domain)

    return {
        'domain': f"{parsed.scheme}://{domain}",
        'pages': sorted(crawler.visited_urls)
    }