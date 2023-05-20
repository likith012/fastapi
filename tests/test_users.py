from app import schemas, models


def test_create_user(client):
    response = client.post(
        "/users/",
        json={"email": "hello@gmail.com", "username": "hellouser", "password": "hello"},
    )
    new_user = schemas.UserCreateOut(**response.json())
    assert response.status_code == 201
    assert new_user.email == "hello@gmail.com"
    assert new_user.username == "hellouser"


def test_session(session):
    new_user = models.User(
        username="hellouser", email="hello@gmail.com", password="hello"
    )
    session.add(new_user)
    session.commit()
    query = session.query(models.User).filter(models.User.username == "hellouser")
    assert query.first().email == "hello@gmail.com"
    assert query.first().password == "hello"


def test_get_users(client, user_create):
    response = client.get("/users/")
    users = [schemas.UserGetOut(**user) for user in response.json()]
    assert response.status_code == 200
    assert len(response.json()) == 1 and len(users) == 1
    assert users[0].email == "hello@gmail.com"


def test_get_user(client, user_create):
    response = client.get("/users/1/")
    user = schemas.UserGetOut(**response.json())
    assert response.status_code == 200
    assert user.email == "hello@gmail.com"
