from src.web_crawler_server import WebCrawler

def test_is_valid_url():
    crawler = WebCrawler()
    assert crawler.is_valid_url('http://example.com')
    assert not crawler.is_valid_url('not-a-url')

def test_extract_links():
    html = """
    <html>
        <body>
            <a href="/page1">Page 1</a>
            <img src="/img.png">
        </body>
    </html>
    """
    crawler = WebCrawler()
    base_url = 'http://example.com'
    links = crawler.extract_links(html, base_url)
    assert 'http://example.com/page1' in links
    assert 'http://example.com/img.png' in links
