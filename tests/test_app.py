import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app, activities


def test_unregister_participant_from_activity():
    client = TestClient(app)
    activity = activities["Chess Club"]
    original_participants = list(activity["participants"])

    try:
        response = client.post(
            "/activities/Chess Club/unregister?email=michael@mergington.edu"
        )

        assert response.status_code == 200
        assert "michael@mergington.edu" not in activity["participants"]
        assert len(activity["participants"]) == len(original_participants) - 1
    finally:
        activity["participants"] = original_participants
