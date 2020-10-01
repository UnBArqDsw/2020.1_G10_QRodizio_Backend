from qrodizio.models import Employee

def test_employees_get_all(client):
    """Test get all employees"""
    # Act
    response = client.get("/employees/")

    # Assert
    assert response.status_code == 200
    data = response.json["employees"]
    assert len(data) == 2

    assert data[0]["name"] == "Fulano"
    assert data[1]["name"] == "Ciclano"


def test_employees_get_one(client):
    employees = Employee.query.all()

    for employee in employees:
        response = client.get(f"/employees/{employee.id}")

        data = response.get_json()

        assert response.status_code == 200
        assert data["id"] == employee.id
        assert data["name"] == employee.name
        assert data["email"] == employee.email
