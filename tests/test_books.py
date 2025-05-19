def test_create_book(client, auth_headers):
    """Тест создания книги"""
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "quantity": 3
    }
    response = client.post(
        "/books/",
        json=book_data,
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == book_data["title"]
    assert data["author"] == book_data["author"]


def test_get_books(client, auth_headers):
    """Тест получения списка книг"""
    client.post(
        "/books/",
        json={"title": "Sample Book", "author": "Author", "quantity": 1},
        headers=auth_headers
    )

    response = client.get("/books/all")
    assert response.status_code == 200
    books = response.json()
    assert len(books) > 0
    assert books[0]["title"] == "Sample Book"


def test_book_workflow(client, auth_headers):
    """Полный тест работы с книгой (CRUD)"""
    create_res = client.post(
        "/books/",
        json={"title": "CRUD Book", "author": "CRUD Author", "quantity": 5},
        headers=auth_headers
    )
    book_id = create_res.json()["id"]

    get_res = client.get(f"/books/{book_id}")
    assert get_res.status_code == 200
    assert get_res.json()["title"] == "CRUD Book"

    update_res = client.put(
        f"/books/{book_id}",
        json={"title": "Updated", "author": "Updated", "quantity": 10},
        headers=auth_headers
    )
    assert update_res.status_code == 200
    assert update_res.json()["title"] == "Updated"

    del_res = client.delete(
        f"/books/{book_id}",
        headers=auth_headers
    )
    assert del_res.status_code == 200

    verify_res = client.get(f"/books/{book_id}")
    assert verify_res.status_code == 404
