import json

from qrodizio.builders import (
    employee_builder,
    menus_builder,
    demand_builder,
    customer_tables_builder,
    paymentsDemand_builder,
)


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


def get_demands():
    """Read data from dummy_demands.json and parses it to [Demand]"""
    dummy_path = "qrodizio/populate_data/dummy_demands.json"

    with open(dummy_path) as dummy_io:
        dummy_data = json.loads(dummy_io.read())

        demands = []
        for demand_data in dummy_data["demands"]:
            demand = demand_builder(**demand_data)
            demands.append(demand)

    return demands


def get_customer_tables():
    dummy_path = "qrodizio/populate_data/dummy_customer_tables.json"

    with open(dummy_path) as dummy_io:
        dummy_data = json.loads(dummy_io.read())
        customer_tables = []

        for customer_table_data in dummy_data["customer_tables"]:
            customer_table = customer_tables_builder(**customer_table_data)
            customer_tables.append(customer_table)

    return customer_tables

def get_paymentsDemand():
    dummy_path = "qrodizio/populate_data/dummy_payment_tables.json"

    with open(dummy_path) as dummy_io:
        dummy_data = json.loads(dummy_io.read())
        table_payment = []

        for table_payment_data in dummy_data["table_payment"]["customer_payment"]:
            table_payment = paymentsDemand_builder(**table_payment_data)
            table_payments.append(table_payment)
