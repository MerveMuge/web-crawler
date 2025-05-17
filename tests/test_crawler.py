import unittest

from src.web_crawler_server import WebCrawler

class TestWebCrawler(unittest.TestCase):

    def setUp(self):
        self.crawler = WebCrawler()

    def test_extract_links_should_return_absolute_urls(self):
        html = """
        <html>
            <body>
                <a href="/page1">Page 1</a>
                <img src="/img.png">
            </body>
        </html>
        """
        base_url = 'http://example.com'
        links = self.crawler.extract_links(html, base_url)

        self.assertIn('http://example.com/page1', links)
        self.assertIn('http://example.com/img.png', links)

    def test_extract_links_should_ignore_tags_without_href_or_src(self):
        """Ensure tags without href or src are ignored"""
        html = """
        <html>
            <body>
                <a>Missing href</a>
                <img>
                <script></script>
            </body>
        </html>
        """
        base_url = 'http://example.com'
        links = self.crawler.extract_links(html, base_url)

        self.assertEqual(len(links), 0)  # Should return an empty set

class TestNormalizeURL(unittest.TestCase):

    def setUp(self):
        self.crawler = WebCrawler()

    def test_normalize_url_should_lowercase_scheme_and_domain(self):
        self.assertEqual(
            self.crawler.normalize_url("HTTPS://Example.COM/Page"),
            "https://example.com/Page"
        )

    def test_normalize_url_should_remove_trailing_slash(self):
        self.assertEqual(
            self.crawler.normalize_url("https://example.com/page/"),
            "https://example.com/page"
        )

    def test_normalize_url_should_remove_fragment(self):
        self.assertEqual(
            self.crawler.normalize_url("https://example.com/page#section"),
            "https://example.com/page"
        )

    def test_normalize_url_should_remove_query_string(self):
        self.assertEqual(
            self.crawler.normalize_url("https://example.com/page?id=123"),
            "https://example.com/page"
        )

    def test_normalize_url_should_handle_combined_case(self):
        self.assertEqual(
            self.crawler.normalize_url("HTTP://Example.com/Page/?id=1#top;v=2"),
            "http://example.com/Page"
        )

    def test_normalize_url_should_handle_root_url(self):
        self.assertEqual(
            self.crawler.normalize_url("https://Example.com/"),
            "https://example.com"
        )

class TestIsValidUrl(unittest.TestCase):
    def setUp(self):
        self.crawler = WebCrawler()

    def test_is_valid_url_should_return_true_for_valid_http_url(self):
        """Check that a standard HTTP URL is valid"""
        assert self.crawler.is_valid_url('http://example.com')


    def test_is_valid_url_should_return_false_for_invalid_string(self):
        """Check that an invalid string returns False"""
        assert not self.crawler.is_valid_url('not-a-url')