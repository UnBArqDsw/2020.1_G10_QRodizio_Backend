from flask_socketio import send, emit
from flask import request
from qrodizio.ext.socketio import socketio

from qrodizio.singletons import employee_pool


@socketio.on("employee_logged")
def socktio_employee_logged(employee):
    print("<>" * 80)
    print(f"FROM: {request.sid}")
    print("logged employee json: " + str(employee))
    print("<>" * 80)

    logged_employee = {"sid": request.sid, **employee}
    employee_pool.add_employee(logged_employee)
    emit("frontend_employee_logged", logged_employee, json=True)
