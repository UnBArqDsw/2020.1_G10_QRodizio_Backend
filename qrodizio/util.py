from qrodizio.models.users import Employee
from qrodizio.ext.authentication import hash_password


def employee_builder(**employee_attrs):
    """Instantiate an Employee, setts its attributes and hashes its pasword"""
    employee = Employee()

    for key in employee_attrs.keys():
        setattr(employee, key, employee_attrs[key])

    employee.password = hash_password(employee.password)

    return employee
