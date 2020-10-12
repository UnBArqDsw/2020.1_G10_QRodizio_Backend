from .util import get_user_token
from qrodizio.models import Employee


def test_employees_get_all(client):
    """Test get all employees"""
    # Get user token
    user_token = get_user_token(client, "fulano@email.com", "fulano")

    # Act
    response = client.get(
        "/employees/",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    # Assert
    assert response.status_code == 200
    data = response.json["employees"]
    assert len(data) == Employee.query.count()


def test_employees_get_one(client):
    """Test get one employee"""
    user_token = get_user_token(client, "fulano@email.com", "fulano")
    employee = Employee.query.first()

    response = client.get(
        f"/employees/{employee.id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    data = response.get_json()

    assert response.status_code == 200
    assert data["id"] == employee.id
    assert data["name"] == employee.name
    assert data["email"] == employee.email
    assert "password" not in data.keys()


def test_employees_get_one_requires_auth(client):
    """Must be logged to get one employee"""
    employee = Employee.query.first()

    response = client.get(
        f"/employees/{employee.id}",
    )

    assert response.status_code == 401

    user_token = get_user_token(client, "fulano@email.com", "fulano")

    response = client.get(
        f"/employees/{employee.id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert response.status_code == 200
    assert response.json["id"] == employee.id
    assert response.json["name"] == employee.name
    assert response.json["email"] == employee.email
    assert "password" not in response.json.keys()
