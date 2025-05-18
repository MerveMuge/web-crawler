# Web Crawler API

A lightweight web crawler built with FastAPI.

Give it a URL — it crawls all pages under the same domain and returns a list of unique links in JSON format.

---

##  Key Features

-  GET endpoint: `/pages?target=<url>`
-  Crawls only within the same domain
-  Built-in Swagger UI (/docs) for interactive testing
-  Skips broken, slow, or invalid URLs 
-  URL normalization (removes query params, fragments, etc.)

---

## Requirements

- `fastapi` – Web framework
- `uvicorn` – ASGI server to run FastAPI
- `requests` – For making HTTP requests
- `beautifulsoup4` – HTML parsing
- `pytest` – Testing framework

Install with:

```bash
  pip install -r requirements.txt
```
## How to Run
```bash
  uvicorn src.main:app --reload
```

## Run Rests
```bash
  PYTHONPATH=src python3 -m pytest 
```

## Example Usage
You can test the API using curl:
```
curl -X 'GET' \
  'http://127.0.0.1:8000/pages?target=https%3A%2F%2Fexample.com' \
  -H 'accept: application/json'
```
Response:
```
{
  "domain": "https://example.com",
  "pages": [
    "https://example.com"
  ]
}
```

## Interactive API Docs
FastAPI auto-generates Swagger UI for easy exploration: http://localhost:8000/docs

## Future Improvements

- Support for robots.txt

  Read and follow rules defined by websites to avoid crawling restricted or sensitive areas.
- Set limits for max crawl depth and total pages
- Switch to async crawling for better performance (e.g. with httpx)
- Add option to save/export results (e.g. JSON or CSV)
- Add content parsing 

    After downloading a page, it should be parsed into a structured format.
Parsing also acts as validation — helping to filter out broken, malformed, or irrelevant HTML pages before storing or analyzing them.
- Detect duplicate content (Content Seen)

    Currently, the crawler checks if a URL has been visited, but not if the content is identical across different URLs.
Hashing the page body (e.g., using SHA-256) would allow the crawler to skip duplicate pages even when the URL is unique.
