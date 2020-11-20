from flask_socketio import emit
from flask import request

from qrodizio.ext.socketio import socketio
from qrodizio.singletons import employee_pool
from qrodizio.models.tables import TableSession


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


@socketio.on("call_for_assistance")
def call_for_assistance(url):
    query = TableSession.query.filter_by(url=url).first()

    if query == None:
        print("<>" * 80)
        print("Table session not found")
        print("<>" * 80)

        # nofity table
        emit("frontend_employee_called", "Table session not found", json=True)
        return

    #So manda msg
    emit("frontend_employee_called", "Employee called", json=True)  # nofity table

    #Notifica
    emit(  # notify employees
        "frontend_call_for_employee_on_table",
        {"session": query.to_dict()},
        json=True,
        broadcast=True,
    )

@socketio.on("response_for_assistence")
def response_for_assistence(url):
    query = TableSession.query.filter_by(url=url).first()

    if query == None:
        print("<>" * 80)
        print("Table session not found")
        print("<>" * 80)

        # nofity table
        emit("frontend_employee_called", "Table session not found", json=False)
        return

    #So manda msg
    emit("frontend_employee_called", "O cliente agradece", json=True)  # nofity table

    emit(  # notify employees
        "frontend_not_call_for_employee_on_table",
        {"session": query.to_dict()},
        json=False,
        broadcast=True,
    )
