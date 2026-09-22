from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "newstudent@example.com"
    activity = activities[activity_name]
    original_participants = list(activity["participants"])

    try:
        # Arrange: the participant should not already be registered.
        if email in activity["participants"]:
            activity["participants"].remove(email)

        # Act: sign up the participant.
        signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert: the signup succeeds and updates the in-memory list.
        assert signup_response.status_code == 200
        assert email in activity["participants"]

        # Act: unregister the participant.
        delete_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

        # Assert: the participant is removed from the activity.
        assert delete_response.status_code == 200
        assert email not in activity["participants"]
    finally:
        activity["participants"] = original_participants
