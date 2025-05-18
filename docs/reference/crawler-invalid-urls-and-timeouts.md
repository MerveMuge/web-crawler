# Handling Invalid URLs, Timeouts & Network Errors
Web pages don’t always respond as expected. Some links are broken, some time out, and others may use unsupported formats. The crawler is designed to handle these cases gracefully — it skips bad URLs and continues without crashing or stopping the crawl.


## Current Implementation
The crawler wraps requests in a try-except block to catch common failures such as:

* Invalid URLs (bad format or missing scheme)
* Timeout errors
* SSL problems (expired, self-signed, wrong domain)
* Network-related exceptions (e.g., unreachable hosts)

If a request fails for any reason:

- The error is logged
- The crawler moves on to the next link
- A timeout (e.g., 5 seconds) is set using `requests.get(url, timeout=5)` to prevent the crawler from hanging too long.

### Where SSL Checking Happens
```
response = requests.get(url, timeout=5)
```

the requests library performs an HTTPS handshake. This includes:

- Validating the server’s SSL certificate
- Checking if it:
  - Is signed by a trusted CA
  - Is not expired
  - Matches the domain name
  - Has a valid certificate chain

If the certificate is invalid (e.g., self-signed or expired), an SSLError is raised and handled safely.

### Common Network Exceptions

These errors are raised when the crawler can’t connect to the server:


| Type                         | Description                                 | Example Error                 |
|------------------------------|---------------------------------------------|-------------------------------|
| `ConnectionError`            | Can't reach the server at all               | DNS failure, host unreachable |
| `ConnectionRefusedError`     | Server refuses the connection               | Web server is down            |
| `NewConnectionError` | Couldn't open a new TCP connection          | Invalid IP or closed port     |
| `ReadTimeout`                | Connected, but server didn’t respond in time | Very slow or stuck request    |

All of these are caught under requests.exceptions.RequestException, so the crawler logs the issue and continues crawling other pages.


## Future Improvement

### Retry mechanism

Some errors are temporary — retrying may help. The crawler can be extended to:
- Retry failed requests (e.g., 2–3 times)
- Add a short delay between attempts
- Skip the link if all retries fail

``` python
import time

def fetch_with_retries(self, url, max_retries=3, delay=1):
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response
            else:
                logging.warning("Non-200 response (%d) on attempt %d for URL: %s", response.status_code, attempt, url)
                return None
        except requests.exceptions.RequestException as e:
            logging.warning("Attempt %d failed for URL: %s (%s)", attempt, url, e)
            time.sleep(delay)
    logging.error("All %d retry attempts failed for URL: %s", max_retries, url)
    return None
```

replace `response = requests.get(url, timeout=5)` to 
```
response = self.fetch_with_retries(url)
if response is None:
    return
```


### Custom URL validation 
To avoid wasting requests on unsupported or broken links, the URL validation function can be extended to reject:
- mailto:, javascript:, tel: — not real web pages
- Empty strings or fragment-only links ("#", "#section")
- (If Applicable) Static files like .css, .jpg, .pdf, etc.

`<a href="mailto:someone@example.com">Email</a>` -> Not Valid - not crawlable
<br>
`<a href="javascript:void(0)" onclick="openMenu()">Menu</a>` -> Not Valid- Executes JavaScript instead of opening a URL.
<br>
`<a href="#footer">Go to footer</a>`                 -> Not Valid - Fragment only

#### Why This Matters:
- Saves bandwidth
- Reduces errors
- Focuses the crawl on actual HTML pages

### Metrics and Reporting 

Tracking metrics helps monitor performance and spot issues.

#### Example of Useful Metrics

| Metric                     | Description                              |
|----------------------------|------------------------------------------|
|  Total URLs crawled        | How many pages were processed            |
|  Total URLs failed         | How many pages failed and why            |
|  Requests per second (RPS) | Crawl speed                              |
|  Average response time     | 	Page load performance                   |
|  Error types               | Breakdown: timeouts, SSL, etc.           |
|  Retry counts              | How many pages needed retries|
|  Pages per domain          | Per-site stats (if crawling multiple sites)   |

Example Summary Output
```json
{
  "summary": {
    "total_pages_crawled": 182,
    "total_failures": 7,
    "errors": {
      "timeout": 3,
      "ssl_error": 1,
      "request_exception": 2,
      "other": 1
    },
    "average_response_time": 1.23,
    "max_depth_reached": 3
  }
}
```
#### Advanced Tools: Prometheus + Grafana :	Real-time dashboards for metrics

For real-time monitoring:
- Prometheus collects metrics by scraping a /metrics endpoint
- Grafana displays those metrics in live dashboards
