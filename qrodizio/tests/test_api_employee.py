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
    assert len(data) == 2

    assert data[0]["name"] == "Fulano"
    assert data[1]["name"] == "Ciclano"


def test_employees_get_one(client):
    user_token = get_user_token(client, "fulano@email.com", "fulano")
    employees = Employee.query.all()

    for employee in employees:
        response = client.get(
            f"/employees/{employee.id}",
            headers={"Authorization": f"Bearer {user_token}"},
        )

        data = response.get_json()

        assert response.status_code == 200
        assert data["id"] == employee.id
        assert data["name"] == employee.name
        assert data["email"] == employee.email
