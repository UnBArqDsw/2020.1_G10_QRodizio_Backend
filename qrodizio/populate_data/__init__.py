import json

from qrodizio.util import employee_builder, menus_builder


def get_employees():
    """Read data from dummy_employees.json and parses it to [Employee]"""
    dummy_path = "qrodizio/populate_data/dummy_employees.json"

    with open(dummy_path) as dummy_io:
        dummy_data = json.loads(dummy_io.read())

        employees = []
        for employee_data in dummy_data["employees"]:
            employee = employee_builder(**employee_data)
            employees.append(employee)

    return employees


def get_menus():
    """Read data from dummy_menus_with_items.json and parses it to [Menu]"""
    dummy_path = "qrodizio/populate_data/dummy_menus_with_items.json"

    with open(dummy_path) as dummy_io:
        dummy_data = json.loads(dummy_io.read())

        menus = []
        for menu_data in dummy_data["menus"]:
            menu = menus_builder(**menu_data)
            menus.append(menu)

    return menus