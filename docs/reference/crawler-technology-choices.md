# Technology & Library Choices

This document outlines the key libraries and technologies used in the crawler, along with the reasoning behind each choice.

##  Why FastAPI?
FastAPI was selected as the web framework due to its balance of simplicity and developer experience.

**Advantages:**
- **Auto-generated API docs**  
  FastAPI automatically serves interactive docs at /docs (Swagger UI) http://localhost:8000/docs.
- **Minimal setup**  
- **Ideal for demonstration**  
  Makes it easy for reviewers to explore the API without diving into the codebase.

## Why requests (not aiohttp or httpx)?
**requests** is a mature, stable, and user-friendly HTTP client.

**Advantages:**
-  Mature, stable
-  Synchronous behavior matches the current recursive crawl logic

 For lightweight or one-off crawling tasks, requests keeps things simple.  
 If the crawler were scaled up or made concurrent, libraries like aiohttp or httpx would be better suited.

## Why BeautifulSoup for HTML parsing?
BeautifulSoup simplifies extraction of links (href, src) and works reliably even when HTML is not perfectly structured — which is common on real-world websites.

**Advantages:**
-  Easy to use and read
-  Robust against broken or malformed HTML

## Why urllib.parse?
Python’s built-in urllib.parse module handles all the URL operations:

- urlparse / urlunparse → for URL normalization
- urljoin → for resolving relative links
- netloc → for domain checking