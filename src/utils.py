from urllib.parse import urlparse, urljoin, urlunparse, urlsplit
from bs4 import BeautifulSoup

class Utils:

    @staticmethod
    def normalize_url(url):
        parsed = urlparse(url)
        # Remove fragment, lowercase domain, strip trailing slash
        normalized = parsed._replace(
            scheme=parsed.scheme.lower(),      # Lowercase scheme (e.g., HTTP → http)
            netloc=parsed.netloc.lower(),      # Lowercase domain (e.g., Example.com → example.com)
            path=parsed.path.rstrip('/'),      # Remove trailing slash from path (/page/ → /page)
            fragment=''                        # Remove fragments (#section, #top) since they don’t affect page content
        )
        return urlunparse(normalized)

    # Check if a given URL is valid and well-formed
    @staticmethod
    def is_valid_url(url):
        try:
            result = urlparse(url)
            # Return True only if the URL has both scheme (e.g., 'http') and netloc (domain)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    @staticmethod
    def extract_links(html, base_url):
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

