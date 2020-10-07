import json

from qrodizio.models import Employee


def get_employees() -> [Employee]:
    """Read data from dummy_employees.json and parses it to [Employee]"""
    dummy_path = "qrodizio/populate_data/dummy_employees.json"

    with open(dummy_path) as dummy_io:
        dummy_data = json.loads(dummy_io.read())

        employees = []
        for employee_data in dummy_data["employees"]:
            employee = Employee()

            for key in employee_data.keys():
                setattr(employee, key, employee_data[key])

            employees.append(employee)

    return employees
