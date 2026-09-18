from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def reset_activities():
    activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]
    activities["Programming Class"]["participants"] = [
        "emma@mergington.edu",
        "sophia@mergington.edu",
    ]
    activities["Gym Class"]["participants"] = [
        "john@mergington.edu",
        "olivia@mergington.edu",
    ]


def test_signup_rejects_duplicate_email():
    reset_activities()

    response = client.post(
        "/activities/Chess Club/signup?email=michael@mergington.edu"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_participant_from_activity():
    reset_activities()

    response = client.delete(
        "/activities/Chess Club/signup?email=daniel@mergington.edu"
    )

    assert response.status_code == 200
    assert "daniel@mergington.edu" not in activities["Chess Club"]["participants"]
    assert response.json()["message"] == "Removed daniel@mergington.edu from Chess Club"
