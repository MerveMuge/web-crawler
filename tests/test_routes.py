import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from src.main import app

@pytest.fixture
def client():
    return TestClient(app)

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
    json_data = response.json()
    assert 'http://example.com/page1' in json_data['pages']