from urllib.parse import urlparse
from collections import deque

import requests
import logging

from src import utils

class WebCrawler:

    def __init__(self):
        # Set to keep track of visited URLs and avoid duplicates
        self.visited_urls = set()

    def crawl(self, start_url, domain):
        queue = deque([utils.normalize_url(start_url)])

        while queue:
            url = queue.popleft()

            # Skip if the URL has already been visited
            if url in self.visited_urls:
                logging.debug("Already visited: %s", url)
                continue
            # Mark the URL as visited
            self.visited_urls.add(url)
            logging.info("Discovered unique URL for crawling: %s", url)

            try:
                # Attempt to fetch the page content with a timeout
                response = requests.get(url, timeout=5)
                # Proceed only if the page was successfully loaded (status code 200); skip all others
                if response.status_code != 200:
                    logging.warning("Non-200 response (%d) from URL: %s", response.status_code, url)
                    continue

                # Extract all valid links from the page
                links = utils.extract_links(response.text, url)

                for link in links:
                    parsed_link = urlparse(link)
                    if parsed_link.netloc == domain:
                        normalized_link = utils.normalize_url(link)
                        if normalized_link not in self.visited_urls:
                            queue.append(normalized_link)

            except requests.exceptions.Timeout:
                logging.warning("Timeout occurred while accessing URL: %s", url)
            except requests.exceptions.SSLError as ssl_err:
                logging.error("SSL error at %s: %s", url, ssl_err)
            except requests.exceptions.RequestException as req_err:
                logging.error("Request failed for %s: %s", url, req_err)
            except Exception as e:
                logging.exception("Unhandled exception while crawling %s: %s", url, e)