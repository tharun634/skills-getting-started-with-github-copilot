from src import app as app_module


def test_get_activities_returns_seeded_activities(client):
    # Arrange
    expected_activity = app_module.activities["Chess Club"]

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json()["Chess Club"] == expected_activity
    assert len(response.json()) == 9


def test_signup_adds_participant(client, activity_url):
    # Arrange
    activity_name = "Basketball Team"
    email = "student@mergington.edu"

    # Act
    response = client.post(activity_url(activity_name), params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for {activity_name}"
    }
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_rejects_duplicate_participant(client, activity_url):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(activity_url(activity_name), params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student is already signed up"}


def test_signup_rejects_unknown_activity(client, activity_url):
    # Arrange
    activity_name = "Unknown Club"

    # Act
    response = client.post(
        activity_url(activity_name),
        params={"email": "student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_requires_email(client, activity_url):
    # Arrange
    activity_name = "Basketball Team"

    # Act
    response = client.post(activity_url(activity_name))

    # Assert
    assert response.status_code == 422


def test_unregister_removes_participant(client, activity_url):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(activity_url(activity_name), params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from {activity_name}"
    }
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_rejects_participant_not_signed_up(client, activity_url):
    # Arrange
    activity_name = "Basketball Team"
    email = "student@mergington.edu"

    # Act
    response = client.delete(activity_url(activity_name), params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not signed up"}


def test_unregister_rejects_unknown_activity(client, activity_url):
    # Arrange
    activity_name = "Unknown Club"

    # Act
    response = client.delete(
        activity_url(activity_name),
        params={"email": "student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
