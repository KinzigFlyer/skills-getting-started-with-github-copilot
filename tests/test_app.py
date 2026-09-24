from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def reset_activity(activity_name, participants):
    activities[activity_name]["participants"] = list(participants)


def test_signup_for_activity_success():
    activity_name = "Soccer Team"
    email = "student@mergington.edu"
    reset_activity(activity_name, [])

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"


def test_signup_for_activity_rejects_duplicate():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    reset_activity(activity_name, ["michael@mergington.edu", "daniel@mergington.edu"])

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_activity_rejects_full_activity():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    reset_activity(activity_name, ["a@mergington.edu", "b@mergington.edu", "c@mergington.edu"])
    activities[activity_name]["max_participants"] = 3

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"


def test_signup_for_activity_not_found():
    response = client.post("/activities/Unknown Activity/signup?email=student@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


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
