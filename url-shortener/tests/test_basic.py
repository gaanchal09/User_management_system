import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test the root health endpoint."""
    resp = client.get('/')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['status'] == 'healthy'
    assert 'URL Shortener' in data['service']

def test_shorten_url_success(client):
    """Test successful shortening of a valid URL."""
    url = 'https://www.example.com'
    resp = client.post('/api/shorten', json={'url': url})
    assert resp.status_code == 201
    data = resp.get_json()
    assert 'short_code' in data
    assert data['short_url'].startswith('http://localhost:5000/')

def test_shorten_url_invalid(client):
    """Test shortening with invalid URL input."""
    resp = client.post('/api/shorten', json={'url': 'invalid-url'})
    assert resp.status_code == 400
    data = resp.get_json()
    assert 'error' in data

def test_redirect_success_and_click_increment(client):
    """Test redirecting a short code and incrementing clicks."""
    # First, shorten a URL
    url = 'https://www.example.com'
    resp = client.post('/api/shorten', json={'url': url})
    short_code = resp.get_json()['short_code']

    # Stats before redirect: clicks should be 0
    stats_resp = client.get(f'/api/stats/{short_code}')
    stats = stats_resp.get_json()
    assert stats['clicks'] == 0

    # Redirect
    redirect_resp = client.get(f'/{short_code}')
    assert redirect_resp.status_code == 302
    assert redirect_resp.headers['Location'] == url

    # Stats after redirect: clicks should be 1
    stats_resp = client.get(f'/api/stats/{short_code}')
    stats = stats_resp.get_json()
    assert stats['clicks'] == 1

def test_redirect_not_found(client):
    """Test redirect with invalid short code."""
    resp = client.get('/nonexistent')
    assert resp.status_code == 404

def test_stats_not_found(client):
    """Test analytics for non-existent short code."""
    resp = client.get('/api/stats/nonexistent')
    assert resp.status_code == 404
    data = resp.get_json()
    assert 'error' in data
