from fastapi.testclient import TestClient

from src.app import app, activities


def test_unregister_participant_removes_email_from_activity():
    client = TestClient(app)
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    initial_count = len(activities[activity_name]["participants"])

    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == initial_count - 1


def test_signup_rejects_when_activity_is_full():
    client = TestClient(app)
    activity_name = "Chess Club"
    activity = activities[activity_name]
    original_participants = activity["participants"][:]

    activity["participants"] = [f"student{i}@mergington.edu" for i in range(activity["max_participants"])]

    try:
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": "newstudent@mergington.edu"},
        )
    finally:
        activity["participants"] = original_participants

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"
