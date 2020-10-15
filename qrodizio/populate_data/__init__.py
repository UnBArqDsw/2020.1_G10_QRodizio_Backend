import json

from qrodizio.util import employee_builder, menus_builder, costumer_tables_builder


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


def get_costumer_tables():
    dummy_path = "qrodizio/populate_data/dummy_costumer_tables.json"

    with open(dummy_path) as dummy_io:
        dummy_data = json.loads(dummy_io.read())

        costumer_tables = []
        for costumer_table_data in dummy_data["costumer_tables"]:
            costumer_table = costumer_tables_builder(**costumer_table_data)
            costumer_tables.append(costumer_table)
    
    return costumer_tables