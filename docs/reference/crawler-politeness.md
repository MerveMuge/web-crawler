# How to Prevent DDoS-Like Behavior from a Web Crawler

A crawler that sends too many requests too quickly can unintentionally behave like a DDoS (Distributed Denial of Service) attacker — especially when targeting small websites or those with limited resources.

To crawl responsibly and ethically, a few smart design choices help reduce load and respect target servers.

##  Improvements to Reduce Server Load

### Maximum Crawl Depth
Limit how deep the crawler can go from the starting page. For example, stop after 3 levels of links.

### Page Limit

Stop the crawl after visiting a certain number of pages (e.g., 500).  
This protects both the crawler and the website from unnecessary load.

It prevents:
- Overloading your own system
- Risk of being flagged as abusive

### Request Throttling (Delays Between Requests)

Add a short delay between requests to slow down the crawl rate.

- `time.sleep(1)`  
  Good for simple scripts. It pauses everything for 1 second before the next request.

- `await asyncio.sleep(1)`  
  Used in async crawlers — it pauses without blocking other tasks. More efficient for large-scale or parallel crawls.

This helps prevent the crawler from bombarding a server with back-to-back requests.

### Respect robots.txt

Most websites publish a `robots.txt` file to indicate which parts of the site crawlers can or cannot access.

Although not enforced, following `robots.txt` is a widely accepted best practice that shows your crawler is respectful and ethical.

#### Example: `https://example.com/robots.txt`
```
User-agent: *
Disallow: /private/
Allow: /public/
Crawl-delay: 10
```


|             Line             |                  Meaning                  | 
|:----------------------------:|:-----------------------------------------:|
|        User-agent: *         |          Applies to all crawlers          |
|     Disallow: /private/      |     Don’t visit pages under /private/     | 
|     Allow: /public/          |  Crawlers are allowed to access /public/  | 
|       Crawl-delay: 10        | Wait at least 10 seconds between requests | 


