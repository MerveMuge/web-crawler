# What happens if a URL is invalid or times out?
If a URL is invalid or times out, my crawler is designed to gracefully skip it and continue with the rest of the crawl. This is important to ensure the crawler doesn’t crash or hang due to one bad link.


## Current Implementation
The crawler wraps requests in a try-except block to catch common failures such as:

* Invalid URLs (bad format or missing scheme)
* Timeout errors
* SSL certificate issues (Expired certificates, Self-signed certificates, Mismatched domain names, Untrusted certificate authorities, Missing or invalid TLS versions)
* Network-related exceptions (e.g., unreachable hosts)

When a request fails:

If any error occurs (timeout, SSL, bad response, etc.), it logs the issue and calls return.

That return exits the current call to crawl(...), but the rest of the links in the loop still run.

A timeout limit (e.g., 5 seconds) is set on every request using requests.get(url, timeout=5) to avoid hanging on slow responses.

### Where SSL verification happens
```
response = requests.get(url, timeout=5)
```

Under the hood, requests performs an HTTPS handshake that includes:

* Validating the server’s SSL certificate

* Checking if the certificate:
  * Is signed by a trusted Certificate Authority (CA)
  * Is not expired
  * Matches the domain name
  * Has a valid chain of trust

So, if a site has:

* A self-signed certificate
* An expired certificate
* A certificate not issued for the domain

then requests.get(...) will raise: requests.exceptions.SSLError

### What Are Network-Related Exceptions?

These are exceptions that happen due to issues in connectivity between your crawler and the target server.

They typically include:

| Type                         | Description                                 | Example Error                  |
|------------------------------|---------------------------------------------|--------------------------------|
| `ConnectionError`            | Can't reach the server at all               | DNS failure, host unreachable |
| `ConnectionRefusedError`     | Target server refuses the connection        | Web server down               |
| `NewConnectionError` (urllib3) | Couldn't open a new TCP connection          | Invalid IP, dropped connection|
| `ReadTimeout`                | Connected, but server didn’t respond in time | Very slow site or hanging     |

All of the above network-related exceptions are subclasses of: requests.exceptions.RequestException


## Future Improvement
* Retry mechanism

    Retry failed URLs a limited number of times (e.g., 2–3 attempts) before skipping, to account for temporary network glitches.

* Custom URL validation 

    Extend the is_valid_url() method to reject URLs that:

    Use unsupported schemes like mailto: or javascript:

    Are empty or contain only fragments

    Point to non-HTML assets (optional)

* Metrics and reporting 

   Track how many URLs failed and for what reason — helpful for debugging or performance reviews.

### Retry Mechanism
A retry mechanism is a common and practical way to make your crawler more resilient to temporary network issues, like dropped connections or slow servers.
* Tries the request again after a short delay
* Limits the number of retry attempts to avoid infinite loops

#### Implementation Sketch 
##### Wrap requests.get() in a retry loop

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

### Custom URL Validation
A robust crawler should avoid wasting resources on invalid or irrelevant links. The is_valid_url() method can be extended to apply custom rules that go beyond checking for scheme and domain.

#### Reject unsupported schemes
* 1. mailto:, javascript:, ftp:, tel:

  These are not actual web pages and cannot be crawled via HTTP(S).

  `<a href="mailto:someone@example.com">Email</a>`

  `<a href="javascript:void(0)" onclick="openMenu()">Menu</a>` 
    
  Executes JavaScript instead of opening a URL.
  
  Clicking the link calls openMenu(), but does not reload or navigate.

* 2. Reject empty URLs or pure fragments

  `"#", "", "#section"`
 
  These are either:

  * Anchors within the same page
  
  * Placeholder or broken links
  
  They do not lead to new content and should be skipped.
* 3. (Optional) Skip non-HTML/static assets

  `.css, .png, .jpg, .pdf` These are resources, not HTML documents. You can optionally ignore them if your goal is page discovery only.
  
#### Why This Matters
* Reduces HTTP request overhead
* Prevents false-positive errors (e.g., trying to "crawl" a JavaScript function)
* Keeps crawling focused on real web content

### Metrics and Reporting
Metrics are structured, quantitative data points about how your crawler performed.
Reporting is how you collect and present that data (in logs, JSON, dashboards, etc.)

Track metrics like total pages crawled, errors by type, and average response time. These help me monitor crawler health and performance.

#### Possible Metrics to Track

| Metric                     | Description                                                   |
|----------------------------|---------------------------------------------------------------|
|  Total URLs crawled        | Count of all successfully visited pages                      |
|  Total URLs failed         | Count of skipped/errored pages                               |
|  Requests per second (RPS) | How many pages your crawler hits per second                  |
|  Average response time     | Time taken per page (helps diagnose performance or latency)  |
|  Error types               | Breakdown: timeouts, SSL errors, 404s, etc.                  |
|  Retry counts              | How often a page needed multiple attempts                    |
|  Pages per domain          | Useful when crawling multiple websites                       |

Example JSON Summary Report
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
Advanced Tools: Prometheus + Grafana :	Real-time dashboards for metrics

What is Prometheus?

Prometheus is an open-source tool that collects and stores metrics from applications in real time, typically via a /metrics endpoint.

What is Grafana?

Grafana is a dashboarding tool that visualizes metrics from Prometheus and other sources through customizable graphs and alerts.