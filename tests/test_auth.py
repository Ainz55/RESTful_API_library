def test_register_user(client):
    """Тест регистрации нового пользователя"""
    response = client.post(
        "/auth/register",
        json={"email": "new@example.com", "password": "newpass"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_user(client):
    """Тест авторизации пользователя"""
    client.post(
        "/auth/register",
        json={"email": "login@example.com", "password": "loginpass"}
    )

    response = client.post(
        "/auth/login",
        data={"username": "login@example.com", "password": "loginpass"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_protected_route(client, auth_headers):
    """Тест доступа к защищённому маршруту"""

    response = client.get("/books/")
    assert response.status_code == 401
    assert "Not authenticated" in response.json()[
        "detail"]

    response = client.get("/books/", headers=auth_headers)
    assert response.status_code == 200


def test_invalid_token(client, auth_headers):
    """Тест доступа с неверным токеном"""

    response = client.get(
        "/books/",
        headers={"Authorization": "Bearer completely_invalid_token"}
    )
    assert response.status_code == 401
    assert "Not authenticated" in response.json()[
        "detail"]

    valid_token = auth_headers["Authorization"].split()[1]
    corrupted_token = valid_token[
                      :-5] + "abcde"

    response = client.get(
        "/books/",
        headers={"Authorization": f"Bearer {corrupted_token}"}
    )
    assert response.status_code == 401
    assert "Not authenticated" in response.json()[
        "detail"]
