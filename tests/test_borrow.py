def test_borrow_book(client, auth_headers):
    """Тест выдачи книги"""
    book_res = client.post(
        "/books/",
        json={"title": "Borrow Book", "author": "Author", "quantity": 1},
        headers=auth_headers
    )
    book_id = book_res.json()["id"]

    reader_res = client.post(
        "/readers/",
        json={"name": "Test Reader", "email": "reader@test.com"},
        headers=auth_headers
    )
    reader_id = reader_res.json()["id"]

    borrow_res = client.post(
        "/borrow/borrow",
        json={"book_id": book_id, "reader_id": reader_id},
        headers=auth_headers
    )
    assert borrow_res.status_code == 200
    assert borrow_res.json()["return_date"] is None


def test_borrow_limit(client, auth_headers):
    """Тест лимита выдачи книг (3 книги)"""
    reader_res = client.post(
        "/readers/",
        json={"name": "Limit Reader", "email": "limit@test.com"},
        headers=auth_headers
    )
    reader_id = reader_res.json()["id"]

    for i in range(3):
        book_res = client.post(
            "/books/",
            json={"title": f"Book {i}", "author": "Author", "quantity": 1},
            headers=auth_headers
        )
        client.post(
            "/borrow/borrow",
            json={"book_id": book_res.json()["id"], "reader_id": reader_id},
            headers=auth_headers
        )

    book_res = client.post(
        "/books/",
        json={"title": "Fourth Book", "author": "Author", "quantity": 1},
        headers=auth_headers
    )
    response = client.post(
        "/borrow/borrow",
        json={"book_id": book_res.json()["id"], "reader_id": reader_id},
        headers=auth_headers
    )
    assert response.status_code == 400
    assert "Читатель уже взял 3 книги" in response.json()["detail"]
