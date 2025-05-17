# Technology & Library Choices

This document explains the reasoning behind the libraries and frameworks used in the crawler implementation.

##  Why FastAPI?

I chose FastAPI for this project because it combines simplicity with powerful developer tooling — particularly useful in an interview or review setting.

Key Reasons:
- Built-in Swagger UI: FastAPI automatically generates /docs (Swagger) and /redoc endpoints, making the API easy to test, explore, and demonstrate.
- Minimal setup: Like Flask, FastAPI is lightweight and quick to start with — perfect for a single-endpoint project.
- Great for visibility: The auto-generated documentation is ideal for interviews, helping reviewers quickly understand the structure and behavior of the API.

In this context, FastAPI offered better presentation and review capabilities while remaining just as easy to implement as Flask.

## Why `requests` and not `aiohttp` or `httpx`?

**requests** is a mature, stable, and user-friendly HTTP client.

* Easier to debug, widely used 
* Synchronous — matches the simple recursion model used
* Not as fast as async for high-throughput workloads

> For a single-threaded or one-off crawler, `requests` is more than sufficient. If the crawler needed to handle many pages concurrently, `aiohttp` or `httpx` with async would improve performance.

## Why `threading.Lock()`?

Even though the crawler runs synchronously, `threading.Lock()` ensures thread-safe access to the shared `visited` set.

* Useful if multi-threading is added later
* Avoids race conditions and duplicate visits

## Why `BeautifulSoup` for HTML parsing?

* Simple to extract `href` and `src` attributes from various tags
* Handles malformed or real-world HTML better than regex or low-level parsing

> It’s widely supported, easy to read, and effective for most crawling use cases.

## Why `urllib.parse`?

Used for:
* URL normalization (`urlparse`, `urlunparse`)
* Joining relative and absolute links (`urljoin`)
* Extracting domains (`netloc`)

> This standard library module is fast, stable, and avoids external dependencies.

## Summary

This crawler is intentionally built with **simplicity** and **clarity** in mind — perfect for demonstrating problem-solving without overengineering.

If future scaling or performance becomes necessary, each component (Flask, requests, etc.) can be swapped or extended.
