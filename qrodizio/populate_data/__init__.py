import json

from qrodizio.models import Employee
from qrodizio.util import employee_builder


def get_employees() -> [Employee]:
    """Read data from dummy_employees.json and parses it to [Employee]"""
    dummy_path = "qrodizio/populate_data/dummy_employees.json"

    with open(dummy_path) as dummy_io:
        dummy_data = json.loads(dummy_io.read())

        employees = []
        for employee_data in dummy_data["employees"]:
            employee = employee_builder(**employee_data)
            employees.append(employee)

    return employees
