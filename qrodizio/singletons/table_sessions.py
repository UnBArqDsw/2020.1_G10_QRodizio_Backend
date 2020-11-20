from typing import List, Dict, Set
from qrodizio.models.users import Employee


class Customer:
    def __init__(self, name: str, sid: str):
        self.name = name
        self.sid = sid

    def __str__(self):
        return f"{self.name}-{self.sid}"

    def __repr__(self):
        return str(self)


class TableRoom:
    customers = dict()

    def __init__(self, session_url):
        self.session_url = session_url

    def add_customer(self, customer):
        self.customers[customer.sid] = customer

    def remove_customer(self, customer):
        if customer.sid in self.customers:
            del self.customers[customer.sid]


_rooms = {}


def open_or_make_room(session_url) -> TableRoom:
    global _rooms
    room = None

    if session_url in _rooms.keys():
        room = _rooms[session_url]
    else:
        room = TableRoom(session_url)
        _rooms[session_url] = room

    return room
