from fastapi import FastAPI, Query, HTTPException
from urllib.parse import urlparse, urljoin, urlunparse, urlsplit
from bs4 import BeautifulSoup
import requests
import threading
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Web Crawler API")

"""
Web Crawler API (FastAPI)

This FastAPI app exposes an HTTP GET endpoint `/pages` that crawls a website starting from the provided URL.
It returns all unique, valid pages under the same domain.

Example usage:
http://localhost:8000/pages?target=https://example.com
"""
class WebCrawler:

    # Initialize the WebCrawler with a set for visited URLs and a thread lock for safe concurrent access
    def __init__(self):
        # Set to keep track of visited URLs and avoid duplicates
        self.visited = set()

        # Lock to ensure thread-safe operations when accessing the visited set
        self.lock = threading.Lock()

    def normalize_url(self, url):
        parsed = urlparse(url)
        # Remove fragment and query, lowercase domain, strip trailing slash
        normalized = parsed._replace(
            scheme=parsed.scheme.lower(),      # Lowercase scheme (e.g., HTTP → http)
            netloc=parsed.netloc.lower(),      # Lowercase domain (e.g., Example.com → example.com)
            path=parsed.path.rstrip('/'),      # Remove trailing slash from path (/page/ → /page)
            query='',                          # Remove query strings (?id=1) to avoid treating dynamic pages as unique
            fragment=''                        # Remove fragments (#section, #top) since they don’t affect page content
        )
        return urlunparse(normalized)

    # Check if a given URL is valid and well-formed
    def is_valid_url(self, url):
        try:
            result = urlparse(url)
            # Return True only if the URL has both scheme (e.g., 'http') and netloc (domain)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def extract_links(self, html, base_url):
        # Parse the HTML content using BeautifulSoup with the built-in HTML parser
        soup = BeautifulSoup(html, 'html.parser')

        # Find all HTML tags that might contain URLs (e.g., links, scripts, images, etc.)
        tags = soup.find_all(['a', 'link', 'script', 'img', 'iframe'])

        # Initialize an empty set to store discovered URLs (avoids duplicates)
        urls = set()

        # Ensure the base URL ends with a trailing slash if it's a directory-like path.
        #
        # Why this matters:
        # The behavior of urljoin() depends on whether the base URL ends with a slash.
        # - If it ends with '/', it's treated as a directory (e.g., /services/ → /services/page.html)
        # - If it doesn't, it's treated as a file (e.g., /services → /page.html)
        #
        # This logic checks:
        # 1. If the path does NOT already end in a '/'
        # 2. AND the last part of the path does NOT contain a dot (.)
        #    → Meaning it probably isn't a file (like index.html or style.css)
        #
        # If both are true, we assume the URL is a directory path and add the trailing slash
        # to ensure relative links resolve correctly.
        parsed = urlsplit(base_url)
        if not parsed.path.endswith('/') and '.' not in parsed.path.split('/')[-1]:
            base_url += '/'

        # Iterate over all collected HTML tags
        for tag in tags:

            # Check both 'href' and 'src' attributes for potential URLs
            for attr in ['href', 'src']:
                url = tag.get(attr)
                if url:
                    # Convert relative URLs to absolute using the base URL
                    full_url = urljoin(base_url, url)
                    urls.add(full_url)

        # Return the set of unique, fully-qualified URLs found on the page
        return urls

    # Recursively crawl a given URL, staying within the specified domain
    def crawl(self, url, domain):

        # Acquire the lock to safely check and update the visited URLs set
        with self.lock:

            url = self.normalize_url(url)
            # Skip if the URL has already been visited
            if url in self.visited:
                logging.debug("Already visited: %s", url)
                return
            # Mark the URL as visited
            self.visited.add(url)
            logging.info("Discovered unique URL for crawling: %s", url)

        logging.debug("Crawling URL: %s | visited=%d", url, len(self.visited))

        try:
            # Attempt to fetch the page content with a timeout
            response = requests.get(url, timeout=5)
            # Proceed only if the page was successfully loaded (status code 200); skip all others
            if response.status_code != 200:
                logging.warning("Non-200 response (%d) from URL: %s", response.status_code, url)
                return

            # Extract all valid links from the page
            links = self.extract_links(response.text, url)

            # Recursively crawl links that belong to the same domain
            for link in links:
                parsed_link = urlparse(link)
                if parsed_link.netloc == domain:
                    self.crawl(link, domain)
        except requests.exceptions.Timeout:
            logging.warning("Timeout occurred while accessing URL: %s", url)
            return
        except requests.exceptions.SSLError as ssl_err:
            logging.error("SSL error at %s: %s", url, ssl_err)
            return
        except requests.exceptions.RequestException as req_err:
            logging.error("Request failed for %s: %s", url, req_err)
            return
        except Exception as e:
            logging.exception("Unhandled exception while crawling %s: %s", url, e)
            return

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
    if not target or not crawler.is_valid_url(target):
        raise HTTPException(status_code=400, detail="Invalid or missing URL")

    # Parse the URL to extract its domain
    parsed = urlparse(target)
    domain = parsed.netloc

    # Start crawling from the target URL, limited to the same domain
    crawler.crawl(target, domain)

    return {
        'domain': f"{parsed.scheme}://{domain}",
        'pages': sorted(crawler.visited)
    }
