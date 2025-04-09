# tests/test_api.py
import os
import requests
from api import login
from unittest.mock import patch

def fake_response(text, status_code):
    """Utility for creating a fake response object."""
    response = requests.Response()
    response._content = text.encode("utf-8")
    response.status_code = status_code
    return response

@patch('api.qbittorrent_api.session.post')
def test_login_success(mock_post):
    # Simulate a successful login returning "Ok." with status 200.
    mock_post.return_value = fake_response("Ok.", 200)
    
    # Set up environment variables.
    os.environ['USERNAME'] = 'test'
    os.environ['PASSWORD'] = 'test'
    os.environ['BASE_URL'] = 'http://fake-url/api/v2'
    
    # Call login() and expect True.
    assert login() is True

@patch('api.qbittorrent_api.session.post')
def test_login_failure(mock_post):
    # Simulate a failed login returning error text like "Not Found" with a 404 error.
    mock_post.return_value = fake_response("Not Found", 404)
    
    os.environ['USERNAME'] = 'test'
    os.environ['PASSWORD'] = 'test'
    os.environ['BASE_URL'] = 'http://fake-url/api/v2'
    
    # Call login() and expect False.
    assert login() is False
