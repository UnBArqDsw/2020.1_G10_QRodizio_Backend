import json

from .util import get_user_token


def test_register_new_employee(client):
    """Test create new employee"""
    email = "newemployee@email.com"
    name = "newemployee"
    password = "newemployee"
    role = "basic"
    user_token = get_user_token(client, "fulano@email.com", "fulano")

    response = client.post(
        "/auth/register",
        data=json.dumps(
            {"email": email, "password": password, "name": name, "role": role}
        ),
        content_type="application/json",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert response.status_code == 201

    employee = response.json["employee"]

    assert employee["name"] == name
    assert employee["email"] == email
    assert "password" not in employee.keys()


def test_only_managers_can_register_new_employees(client):
    """Test if only users with manager role can create new employees"""
    email = "other@email.com"
    name = "other"
    password = "other"
    role = "basic"

    def dispatch_request(**headers):
        return client.post(
            "/auth/register",
            data=json.dumps(
                {"email": email, "password": password, "name": name, "role": role}
            ),
            content_type="application/json",
            **headers,
        )

        return response

    # Act 1: wont allow without authorization
    response = dispatch_request()

    assert response.status_code == 401
    assert response.json["error"] == "User unauthorized"

    # Act 2: wont allow a user that don't have manager role
    user_token = get_user_token(client, "ciclano@email.com", "ciclano")
    response = dispatch_request(headers={"Authorization": f"Bearer {user_token}"})

    assert response.status_code == 403
    assert response.json["error"] == "User unauthorized"

    # Act 3: Will allow a user that has manager role
    user_token = get_user_token(client, "fulano@email.com", "fulano")
    response = dispatch_request(headers={"Authorization": f"Bearer {user_token}"})

    assert response.status_code == 201

    employee = response.json["employee"]

    assert employee["name"] == name
    assert employee["email"] == email
    assert "password" not in employee.keys()


def test_loggin_employee_to_get_token(client):
    """Test get user token"""
    email = "fulano@email.com"
    password = "fulano"

    response = client.post(
        "/auth/loggin",
        data=json.dumps({"email": email, "password": password}),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert "token" in response.json.keys()
    assert len(response.json["token"]) != 0
