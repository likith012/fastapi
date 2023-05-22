from app import schemas


def test_get_all_posts(authorized_client, post_create):
    response = authorized_client.get("/posts/")
    posts = [schemas.ResponseOut(**post) for post in response.json()]
    assert response.status_code == 200
    assert len(response.json()) == len(post_create) and len(posts) == len(post_create)


def test_unauthorized_get_all_posts(client, post_create):
    response = client.get("/posts/")
    assert response.status_code == 401


def test_get_one_post(authorized_client, post_create):
    response = authorized_client.get("/posts/1/")
    post = schemas.ResponseOut(**response.json())
    assert response.status_code == 200
    assert len(post_create) != 1


def test_unauthorized_get_one_post(client, post_create):
    response = client.get("/posts/1/")
    assert response.status_code == 401


def test_get_one_post_not_found(authorized_client, post_create):
    response = authorized_client.get("/posts/999/")
    assert response.status_code == 404


def test_put_one_post(authorized_client, post_create):
    response = authorized_client.put(
        "/posts/1/",
        json={"title": "mellow", "content": "mellow World!", "published": False},
    )
    assert response.status_code == 202
    assert response.json()["title"] == "mellow"
    assert response.json()["content"] == "mellow World!"
    assert response.json()["published"] == False


def test_delete_one_post(authorized_client, post_create):
    response = authorized_client.delete("/posts/1/")
    assert response.status_code == 204


def test_delete_post_not_found(authorized_client, post_create):
    response = authorized_client.delete("/posts/999/")
    assert response.status_code == 404


def test_delete_all_posts(authorized_client, post_create):
    for post_id in range(1, len(post_create) + 1):
        response = authorized_client.delete(f"/posts/{post_id}/")
        assert response.status_code == 204
    response = authorized_client.get("/posts/")
    assert len(response.json()) == 0


def test_create_post(authorized_client, post_create):
    response = authorized_client.post(
        "/posts/",
        json={"title": "mellow", "content": "mellow World!", "published": False},
    )
    assert response.status_code == 201
    assert response.json()["title"] == "mellow"
    assert response.json()["content"] == "mellow World!"
    assert response.json()["published"] == False
