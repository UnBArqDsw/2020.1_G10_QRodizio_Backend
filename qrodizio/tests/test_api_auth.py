import json


def test_register_new_employee(client):
    """Test create new employee"""
    email = "newemployee@email.com"
    name = "newemployee"
    password = "newemployee"

    response = client.post(
        "/auth/register",
        data=json.dumps({"email": email, "password": password, "name": name}),
        content_type="application/json",
    )

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
