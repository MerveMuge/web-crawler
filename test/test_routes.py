from unittest.mock import Mock, patch

import pytest

from src.web_crawler_server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_invalid_url(client):
    response = client.get('/pages?target=invalid-url')
    assert response.status_code == 400

@patch('src.web_crawler_server.requests.get')
def test_valid_crawl(mock_get, client):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = """
        <html>
            <a href="/page1">Page 1</a>
        </html>
    """
    mock_get.return_value = mock_response

    response = client.get('/pages?target=http://example.com')
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'http://example.com/page1' in json_data['pages']