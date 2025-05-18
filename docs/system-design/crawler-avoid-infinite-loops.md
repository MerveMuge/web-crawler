# How to avoid infinite loops 

Web crawlers can easily get stuck in loops — for example, when links point back to previously visited pages or when the structure goes too deep. To avoid this, the crawler uses two main techniques:

## Current Development

###  Visited URL Tracking  
The crawler keeps a set of all URLs it has already visited. Before opening a new page, it checks this set.  
If the URL is already there, it's skipped.  
This stops the crawler from revisiting the same page and getting caught in circular or repeating paths.

### URL Normalization  
Some URLs look different but actually point to the same content. The crawler cleans and standardizes each URL before saving it. For example:

- `/page` vs `/page/` (trailing slash)
- `#section` (fragment)
- `?month=2023-09` (query parameters)

Removing these parts ensures that different versions of the same URL are treated as one — avoiding unnecessary re-crawling.

## Future Improvement

###  Maximum Crawl Depth  
Add a rule to limit how many levels deep the crawler can go.  
For example: start at depth 0, links on that page are depth 1, and so on. If a page is beyond the set depth (like 3), the crawler stops exploring further from that page.

This prevents it from going too deep into endless structures — like calendar archives or infinite scroll sections.

```python 
def crawl(self, url, domain, depth=0, max_depth=3):
    if depth > max_depth:
        return
    # continue crawling...
``` 
Start crawling like this:

```python
self.crawl(start_url, domain, depth=0, max_depth=3)
```

###  Page Limit  

Limit the total number of pages the crawler is allowed to visit — for example, stop after 500 pages.

This protects against massive sites that could overload the crawler.

```python 
def crawl(self, url, domain, depth=0, max_depth=3, max_pages=500):
    if depth > max_depth or len(self.visited_urls) >= max_pages:
        return
    # continue crawling...
``` 

Start crawling like this:
```python 
self.crawl(start_url, domain, depth=0, max_depth=3, max_pages=500)
``` 
