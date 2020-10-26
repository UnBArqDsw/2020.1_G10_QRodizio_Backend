import json
from sqlalchemy import text
from qrodizio.models.menus import Menu, Item


def test_menus_get_all(client):
    """Test get all menus"""
    # Act
    response = client.get("/menus/")

    # Assert
    assert response.status_code == 200
    data = response.json["menus"]
    assert len(data) > 0

    for menu_data in data:
        menu = Menu.query.get(menu_data["id"])

        assert menu_data["name"] == menu.name
        assert len(menu_data["items"]) > 0
        assert len(menu_data["items"]) == len(menu.items)


def test_menus_get_single(client):
    """Test get a single menu"""
    menu = Menu.query.first()

    # Act
    response = client.get(f"/menus/{menu.id}")

    # Assert
    assert response.status_code == 200
    data = response.json["menu"]

    assert data["id"] == menu.id
    assert len(data["items"]) == len(menu.items)


def test_menus_create(client):
    """Test create a menu"""
    post_data = {
        "name": "new menu",
        "description": "the newest menu on the market!",
        "items": [
            {"name": "Item a", "value": 1.0},
            {"name": "Item b", "value": 2.0},
            {"name": "Item c", "value": 3.0},
        ],
    }

    # Act
    response = client.post(
        "/menus/", data=json.dumps(post_data), content_type="application/json"
    )

    # Assert
    assert response.status_code == 201
    data = response.json["menu"]

    menu = Menu.query.get(data["id"])

    assert data["name"] == menu.name
    assert data["description"] == menu.description
    assert len(data["items"]) > 0
    assert len(data["items"]) == len(menu.items)


def test_add_items_to_menu(client):
    """Test add items to menu"""
    menu = Menu.query.first()
    menu_id = menu.id
    old_items_len = len(menu.items)

    put_data = {
        "items": [
            {"name": "Item d", "value": 4.0},
            {"name": "Item e", "value": 5.0},
        ],
    }

    # Act
    response = client.post(
        f"/menus/{menu_id}", data=json.dumps(put_data), content_type="application/json"
    )

    # Assert
    assert response.status_code == 202
    data = response.json["menu"]

    menu = Menu.query.get(menu_id)

    assert data["name"] == menu.name
    assert len(data["items"]) > 0
    assert len(data["items"]) == len(menu.items)
    assert len(menu.items) > old_items_len
    assert data["items"][-1]["name"] == "Item e"
    assert data["items"][-1]["name"] == menu.items[-1].name


def test_edit_menu(client):
    """Test edit menu"""
    menu = Menu.query.first()
    menu_id = menu.id
    menu_old_name = menu.name

    post_data = {"name": "testing with a new name"}

    # Act
    response = client.put(
        f"/menus/{menu_id}", data=json.dumps(post_data), content_type="application/json"
    )

    # Assert
    assert response.status_code == 202
    data = response.json["menu"]

    menu = Menu.query.get(menu_id)

    assert data["name"] != menu_old_name
    assert menu.name != menu_old_name
    assert data["name"] == post_data["name"]
    assert menu.name == post_data["name"]
    assert len(menu.items) > 0
    assert len(data["items"]) > 0
    assert len(menu.items) == len(data["items"])


def test_delete_menu(client):
    """Test delete menu"""
    menu = Menu.query.first()
    menu_id = menu.id
    old_menu_len = Menu.query.count()

    # Act
    response = client.delete(f"/menus/{menu_id}")

    # Assert
    assert response.status_code == 202
    assert response.json["success"] == "menu deleted"
    assert Menu.query.count() < old_menu_len


def test_delete_menu_item(client):
    """Test delete menu item"""
    menu = Menu.query.first()
    menu_id = menu.id
    item_id = menu.items[0].id
    old_items_len = Item.query.count()

    # Act
    response = client.delete(f"/menus/{menu_id}/{item_id}")

    # Assert
    assert response.status_code == 202
    assert response.json["success"] == "menu item deleted"
    assert Item.query.count() < old_items_len


def test_cant_delete_item_from_other_menu(client):
    """Test cant delete an item that belongs to other menu"""
    menu = Menu.query.first()
    menu_id = menu.id
    item = Item.query.order_by(text("-id")).first()  # get last item
    item_id = item.id
    old_items_len = Item.query.count()

    # Act
    response = client.delete(f"/menus/{menu_id}/{item_id}")

    # Assert
    assert response.status_code == 406
    assert response.json["error"] == "Item does not belong to menu"
    assert Item.query.count() == old_items_len
