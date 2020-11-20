from flask_socketio import emit, send, join_room
from flask import request

from qrodizio.ext.socketio import socketio
from qrodizio.singletons import table_sessions
from qrodizio.models.tables import TableSession


@socketio.on("customer_join_room")
def socktio_customer_join_room(data):
    if not "session_url" in data.keys():
        print("<>" * 80)
        print("ERROR: no session_url was given")
        print("<>" * 80)
        return

    name = data.get("name")
    session_url = data.get("session_url")

    customer = table_sessions.Customer(name, request.sid)
    table_room = table_sessions.open_or_make_room(session_url)
    table_room.add_customer(customer)

    join_room(table_room.session_url)

    print("<>" * 80)
    print(f"Customer jointed: {table_room.session_url} | {customer}")
    print("<>" * 80)


@socketio.on("customer_new_demand_sent")
def socketio_customer_new_demand_sent(session_url):
    query = TableSession.query.filter_by(url=session_url).first()

    if query == None:
        print("<>" * 80)
        print("ERROR: no session was found")
        print("<>" * 80)
        return

    demands = [demand.to_dict() for demand in query.demands]

    emit(
        "frontend_table_demands_updated",
        {"demands": demands, "session_url": session_url},
        json=True,
        room=session_url,
    )
