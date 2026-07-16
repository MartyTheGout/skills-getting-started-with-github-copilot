import copy
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app, activities


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def reset_activities():
    original_state = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(original_state))


def test_get_activities_returns_all_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert "Programming Class" in payload


def test_signup_adds_participant(client):
    response = client.post(
        "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
    )

    assert response.status_code == 200
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_rejects_duplicate_participant(client):
    response = client.post(
        "/activities/Chess%20Club/signup?email=michael@mergington.edu"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_unregister_removes_participant(client):
    response = client.post(
        "/activities/Chess%20Club/unregister?email=michael@mergington.edu"
    )

    assert response.status_code == 200
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_rejects_unknown_participant(client):
    response = client.post(
        "/activities/Chess%20Club/unregister?email=notfound@mergington.edu"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student not found"