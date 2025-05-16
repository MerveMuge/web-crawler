# How to avoid infinite loops ?

## Current Development

* Tracking visited URLs to prevent duplicate visits

  Before crawling any URL, I check whether it’s already in that set—if it is, I skip it. This prevents the crawler from revisiting pages and avoids cycles caused by circular or self-referencing links.

* ️ URL normalization to standardize and deduplicate similar URLs 
  * Trailing slashes (/page vs /page/), 
  * Fragments (#section)
  * Query parameters (?month=2023-09))
  * ...
  
  This ensures different-looking URLs pointing to the same content are treated consistently.

## Future Improvement

* Maximum crawl depth to limit recursion and avoid deep link structures (e.g., only follow links 3 levels deep)
* Page limit to stop crawling after a fixed number of pages, protecting against extremely large or dynamically generated sites (e.g., stop after 500 pages)

### How to Define Maximum Crawl Depth

Modify the crawler to track how deep it is in the link hierarchy as it recursively follows pages.

For example, if the starting URL is at depth 0, then any link found on that page is depth 1, and so on. Once the current depth exceeds the defined limit (e.g., 3), the crawler stops following further links from that page.

This prevents the crawler from going too deep into structures like calendar archives, infinite pagination, or deeply nested categories.

```python 
def crawl(self, url, domain, depth=0, max_depth=3):
    if depth > max_depth:
        return
    # continue crawling...
``` 

And when starting the crawl:

```python
self.crawl(start_url, domain, depth=0, max_depth=3)
```
### How to Define a Maximum Page Limit
This prevents the crawler from consuming too many resources on extremely large or dynamically generated sites—such as blogs with thousands of pages.

```python 
def crawl(self, url, domain, depth=0, max_depth=3, max_pages=500):
    if depth > max_depth or len(self.visited) >= max_pages:
        return
    # continue crawling...
``` 

And initiate the crawl like:
```python 
self.crawl(start_url, domain, depth=0, max_depth=3, max_pages=500)
``` 
