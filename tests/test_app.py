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


def test_signup_adds_new_participant():
    # Arrange
    reset_activities()
    email = "student@mergington.edu"

    # Act
    response = client.post(
        "/activities/Chess Club/signup?email=student@mergington.edu"
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Signed up student@mergington.edu for Chess Club"
    assert email in activities["Chess Club"]["participants"]


def test_signup_rejects_duplicate_email():
    # Arrange
    reset_activities()

    # Act
    response = client.post(
        "/activities/Chess Club/signup?email=michael@mergington.edu"
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_participant_from_activity():
    # Arrange
    reset_activities()
    email = "daniel@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/Chess Club/signup?email={email}"
    )

    # Assert
    assert response.status_code == 200
    assert email not in activities["Chess Club"]["participants"]
    assert response.json()["message"] == f"Removed {email} from Chess Club"
