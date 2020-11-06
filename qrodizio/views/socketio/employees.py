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

    employees = employee_pool.get_logged_employees()

    emit("frontend_current_logged_employee", employees, json=True, broadcast=True)


@socketio.on("get_logged_employee")
def socktio_employee_logged(employee):
    employees = employee_pool.get_logged_employees()
    emit("frontend_current_logged_employee", employees, json=True, broadcast=True)


@socketio.on("employee_to_logout")
def socktio_employee_to_logout(employee):
    print("<>" * 80)
    print(f"FROM: {request.sid}")
    print("logout employee: " + str(employee))
    print("<>" * 80)

    employee_pool.remove_employee(employee["id"])
    employees = employee_pool.get_logged_employees()

    emit("frontend_current_logged_employee", employees, json=True, broadcast=True)
