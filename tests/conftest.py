import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_activities():
    """Create a copy of activities for testing to avoid modifying the original"""
    return {
        "Test Club": {
            "description": "A test activity",
            "schedule": "Monday, 3:00 PM",
            "max_participants": 2,
            "participants": ["test1@mergington.edu"]
        }
    }

@pytest.fixture
def mock_activities(monkeypatch):
    """Replace the global activities with test activities"""
    test_data = {
        "Test Club": {
            "description": "A test activity",
            "schedule": "Monday, 3:00 PM",
            "max_participants": 2,
            "participants": ["test1@mergington.edu"]
        }
    }
    monkeypatch.setattr("src.app.activities", test_data)
    return test_data