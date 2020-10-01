def test_home_page(client):
    """Test home page"""
    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200
    status = response.json["status"]
    assert response.json["status"] == "api working"
