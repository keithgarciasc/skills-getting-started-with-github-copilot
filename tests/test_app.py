import pytest
from fastapi.testclient import TestClient

def test_root_redirect(client):
    """Test that root path redirects to static/index.html"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code in (307, 308)  # Both temporary and permanent redirects are fine
    assert response.headers["location"] == "/static/index.html"

def test_get_activities(client, mock_activities):
    """Test getting the list of activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    assert response.json() == mock_activities

def test_signup_success(client, mock_activities):
    """Test successful activity signup"""
    response = client.post("/activities/Test Club/signup?email=new@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "new@mergington.edu" in mock_activities["Test Club"]["participants"]

def test_signup_activity_not_found(client):
    """Test signup for non-existent activity"""
    response = client.post("/activities/Nonexistent Club/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_signup_duplicate(client, mock_activities):
    """Test signing up a participant who is already registered"""
    email = "test1@mergington.edu"  # This email is already in test activities
    response = client.post(f"/activities/Test Club/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()

def test_signup_activity_full(client, mock_activities):
    """Test signing up when activity is at max capacity"""
    # Fill up the activity
    client.post("/activities/Test Club/signup?email=fill@mergington.edu")
    
    # Try to add one more
    response = client.post("/activities/Test Club/signup?email=overflow@mergington.edu")
    assert response.status_code == 400
    assert "full" in response.json()["detail"].lower()

def test_unregister_success(client, mock_activities):
    """Test successful unregistration from activity"""
    email = "test1@mergington.edu"  # This email is in test activities
    response = client.post(f"/activities/Test Club/unregister?email={email}")
    assert response.status_code == 200
    assert email not in mock_activities["Test Club"]["participants"]

def test_unregister_not_registered(client, mock_activities):
    """Test unregistering a participant who isn't registered"""
    response = client.post("/activities/Test Club/unregister?email=notregistered@mergington.edu")
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"].lower()

def test_unregister_activity_not_found(client):
    """Test unregistering from non-existent activity"""
    response = client.post("/activities/Nonexistent Club/unregister?email=test@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"