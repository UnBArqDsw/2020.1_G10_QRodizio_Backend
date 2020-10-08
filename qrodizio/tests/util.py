import json


def get_user_token(client, email, password):
    response = client.post(
        "/auth/loggin",
        data=json.dumps({"email": email, "password": password}),
        content_type="application/json",
    )
    assert response.status_code == 200

    return response.json["token"]
