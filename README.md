# Web Crawler API

This is a lightweight web crawler built with FastAPI. It takes a URL as input and recursively crawls all pages under the **same domain**, returning a list of unique URLs in JSON format.

---

##  Features

-  Single-endpoint API: `GET /pages?target=<url>`
-  Domain-restricted crawling
-  Automatic Swagger UI documentation
-  Error-tolerant (handles timeouts, SSL, broken links)
-  URL normalization (removes fragments, query params, etc.)

---

## Requirements

- `fastapi` – Web framework
- `uvicorn` – ASGI server to run FastAPI
- `requests` – For making HTTP requests
- `beautifulsoup4` – HTML parsing
- `pytest` – Testing framework
- `httpx` - Required by FastAPI's TestClient

Install dependencies:

```bash
pip install -r requirements.txt
```
## How to Run
```bash
cd src
uvicorn web_crawler_server:app --reload
```

## How to Run Rests
```bash
    python3 -m pytest 
```

## Example Usage
Visit in your browser:
```
http://localhost:8000/pages?target=https://example.com
```
returns:
```
{
  "domain": "https://example.com",
  "pages": [
    "https://example.com/",
    "https://example.com/contact.html"
  ]
}
```

## Interactive API Docs
FastAPI automatically generates Swagger UI for testing:
Swagger: http://localhost:8000/docs

## Future Improvements

- Support for robots.txt
- Limit maximum crawl depth and page count
- Async crawling for speed (e.g., using httpx)
- Export results to file