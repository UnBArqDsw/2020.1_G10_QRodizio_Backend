from qrodizio.models.menus import Menu, Item
from qrodizio.models.users import Employee
from qrodizio.models.demands import Demand, DemandStatus
from qrodizio.ext.authentication import hash_password


def employee_builder(**employee_attrs):
    """Instantiate an Employee, setts its attributes and hashes its pasword"""
    employee = Employee()

    for key in employee_attrs.keys():
        setattr(employee, key, employee_attrs[key])

    employee.password = hash_password(employee.password)

    return employee


def menus_builder(**menu_attrs):
    """Instantiate a Menu, setts its attributes and items"""
    menu = Menu()

    if menu_attrs.get("id", None):
        menu = Menu.query.get(menu_attrs["id"])

    menu.name = menu_attrs["name"]
    menu.description = menu_attrs.get("description")
    menu.is_daily = menu_attrs.get("is_daily", False)

    for item_data in menu_attrs["items"]:
        item = _find_item_or_create_one(item_data["name"])

        for key in item_data.keys():
            setattr(item, key, item_data[key])

        menu.items.append(item)

    return menu


def demand_builder(**demand_attrs):
    quantity = demand_attrs.get("quantity", 1)
    status = demand_attrs.get("status", DemandStatus.waiting)
    customer = demand_attrs["customer"]

    if demand_attrs.get("item_id", None):
        item = Item.query.get(item_id)
    else:
        item_name = demand_attrs["item"]
        item = Item.query.filter_by(name=item_name).first()

    demand = Demand(
        quantity=quantity, status=status, item_id=item.id, customer=customer
    )

    return demand


def _find_item_or_create_one(name):
    item = Item.query.filter_by(name=name).first()

    if item == None:
        item = Item()

    return item
