def test_qr_code(client):
    """Test qrcode"""
    # Act
    response = client.get("/qrcode/")

    # Assert
    assert response.status_code == 200
    imagedata = response.json["imagedata"]
    assert len(response.json["imagedata"]) > 10
