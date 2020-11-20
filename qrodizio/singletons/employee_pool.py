from typing import List, Dict
from qrodizio.models.users import Employee

LoggedEmployee = Dict[str, any]

_logged_employees: Dict[int, LoggedEmployee] = dict()


def add_employee(employee: LoggedEmployee):
    global _logged_employees
    _logged_employees[employee["id"]] = employee


def remove_employee(_id: int):
    global _logged_employees

    if _id in _logged_employees:
        del _logged_employees[_id]


def get_logged_employees() -> Dict[int, LoggedEmployee]:
    global _logged_employees
    return _logged_employees


def get_by_id(_id):
    global _logged_employees

    return _logged_employees.get(_id, None)
