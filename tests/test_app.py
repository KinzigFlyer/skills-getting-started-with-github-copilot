from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def reset_activity(activity_name, participants):
    activities[activity_name]["participants"] = list(participants)


def test_unregister_participant_success():
    activity_name = "Chess Club"
    email = "student@mergington.edu"
    reset_activity(activity_name, ["michael@mergington.edu", email, "daniel@mergington.edu"])

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Removed {email} from {activity_name}"


def test_unregister_participant_not_found():
    activity_name = "Programming Class"
    email = "not-registered@mergington.edu"
    reset_activity(activity_name, ["emma@mergington.edu", "sophia@mergington.edu"])

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
