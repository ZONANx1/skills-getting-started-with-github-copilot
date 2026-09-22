from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "newstudent@example.com"
    activity = activities[activity_name]

    if email in activity["participants"]:
        activity["participants"].remove(email)

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200
    assert email in activity["participants"]

    delete_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert delete_response.status_code == 200
    assert email not in activity["participants"]
