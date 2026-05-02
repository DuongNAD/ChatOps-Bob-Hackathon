"""
Pytest configuration and fixtures for testing
"""
import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="module")
def test_client():
    """
    Create a test client for the FastAPI application.
    This fixture is scoped to module level for better performance.
    """
    with TestClient(app) as client:
        yield client


@pytest.fixture
def sample_scan_request():
    """
    Fixture providing a sample scan request payload
    """
    return {
        "url": "https://facebook.com/example",
        "platform": "facebook",
        "data": {"user_id": "123456"}
    }


@pytest.fixture
def minimal_scan_request():
    """
    Fixture providing a minimal scan request (all fields optional)
    """
    return {}


@pytest.fixture
def invalid_scan_request():
    """
    Fixture providing an invalid scan request with wrong data types
    """
    return {
        "url": 12345,  # Should be string
        "platform": ["invalid"],  # Should be string
        "data": "not_a_dict"  # Should be dict
    }

# Made with Bob
