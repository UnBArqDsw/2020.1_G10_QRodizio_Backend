from typing import List, Dict
from qrodizio.models.users import Employee

LoggedEmployee = Dict[str, any]

_logged_employees: List[LoggedEmployee] = []


def add_employee(employee: LoggedEmployee):
    global _logged_employees
    _logged_employees.append(LoggedEmployee)


def get_logged_employees() -> List[LoggedEmployee]:
    global _logged_employees
    return _logged_employees
