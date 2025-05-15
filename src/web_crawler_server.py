from flask import Flask, request, jsonify
from urllib.parse import urlparse, urljoin, urlunparse
from bs4 import BeautifulSoup
import requests
import threading
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO)

# Flask is a lightweight web framework for Python that allows you to build web applications and APIs.
# This line creates a new Flask application instance.
# The __name__ variable helps Flask determine the location of the application so it can find resources like templates.
app = Flask(__name__)

"""
Web Crawler with HTTP Interface using Flask

This Python script runs a web crawler as a local HTTP server using Flask.
It accepts a GET request to /pages?target=<url> and crawls all pages within the same domain.
The crawler:
- Extracts URLs from various HTML attributes (href, src, link, etc.)
- Uses a set to store visited URLs and avoid duplicates
- Is fault-tolerant and skips over inaccessible pages
- Returns a JSON response listing all discovered, unique pages on the domain

Example usage:
http://localhost:5000/pages?target=https://example.com
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
                return
            # Mark the URL as visited
            self.visited.add(url)

        try:
            # Attempt to fetch the page content with a timeout
            response = requests.get(url, timeout=5)
            # Proceed only if the page was successfully loaded (status code 200); skip all others
            if response.status_code != 200:
                return

            # Extract all valid links from the page
            links = self.extract_links(response.text, url)

            # Recursively crawl links that belong to the same domain
            for link in links:
                parsed_link = urlparse(link)
                if parsed_link.netloc == domain:
                    self.crawl(link, domain)
        except Exception as e:
            logging.warning(f"Skipped URL {url} due to: {e}") #broken links, timeouts etc..

# Define an HTTP GET endpoint at /pages that starts the web crawling process
@app.route('/pages')
def get_pages():

    # Get the 'target' URL from the query string (e.g., /pages?target=https://example.com)
    target = request.args.get('target')
    crawler = WebCrawler()

    # Validate the target URL; return a 400 Bad Request error if invalid or missing
    if not target or not crawler.is_valid_url(target):
        return jsonify({'error': 'Invalid or missing URL'}), 400

    # Parse the URL to extract its domain
    parsed = urlparse(target)
    domain = parsed.netloc

    # Start crawling from the target URL, limited to the same domain
    crawler.crawl(target, domain)

    # Return a JSON response containing the domain and the list of discovered pages
    return jsonify({
        'domain': f"{parsed.scheme}://{domain}",
        'pages': sorted(crawler.visited)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
