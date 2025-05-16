# How would you prevent DDoS-like behavior from your crawler?

A web crawler can unintentionally behave like a DDoS (Distributed Denial of Service) agent if it sends too many requests in a short time, especially to small or rate-limited servers.

## Future Improvement

* Maximum crawl depth to limit recursion and avoid deep link structures (e.g., only follow links 3 levels deep)

* Page limit to stop crawling after a fixed number of pages, protecting against extremely large or dynamically generated sites (e.g., stop after 500 pages)

* Request throttling to add a delay between requests. This helps prevent overwhelming target servers with rapid requests and reduces the risk of DDoS-like behavior. This can be implemented using time.sleep() for synchronous code or await asyncio.sleep() in an asynchronous crawler.

* Support for robots.txt to read and respect crawling rules defined by websites. robots.txt is a file websites use to guide crawlers on what they can and can't access. I can optionally add support for it to ensure my crawler respects site rules, avoids private or sensitive areas, and behaves ethically. It's not mandatory, but it's good practice.

### 1. Set a Maximum Crawl Rate

Limit the number of concurrent or total requests:

- Max pages per crawl (e.g., 500)
    
- Max requests per second (e.g., 2–5 rps)

### 2.Define a Maximum Page Limit
This ensures the crawler stops after visiting a fixed number of pages—like 500—even if more links are available.

This prevents:
- Overloading your own system or the target server
- Risk of being blocked or flagged as abusive

### 3. Request Throttling / Delay Between Requests
Add a delay between requests to slow down the crawl rate.

- time.sleep() (synchronous delay)

  With time.sleep(1), your program stops everything for 1 second after each request. Nothing else happens during that pause.

- await asyncio.sleep() (asynchronous delay)  

  With await asyncio.sleep(1), your program starts sleeping, but during that 1 second, it can still fetch another page or do something else — improving efficiency.


## 4. Respect robots.txt (Optional Enhancement)
Check and honor the site’s robots.txt rules if present. Though not enforced, respecting robots.txt is standard etiquette and shows responsibility.

### What is robots.txt?

robots.txt is a special file that websites use to guide web crawlers on which parts of the site they are allowed or not allowed to crawl. It’s located at the root of the site:

It's located at the root of a website, like:
```
https://example.com/robots.txt
```

### Example of a robots.txt file
```
User-agent: *
Disallow: /private/
Allow: /public/
Crawl-delay: 10
```

|             Line             |                  Meaning                   | 
|:----------------------------:|:------------------------------------------:|
|        User-agent: *         |          Applies to all crawlers           |
|     Disallow: /private/      |   Don’t crawl any pages under /private/    | 
|     Allow: /public/          |  Crawlers are allowed to access /public/   | 
|       Crawl-delay: 10        | Wait at least 10 seconds between requests  | 
