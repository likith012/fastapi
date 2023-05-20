import pytest
from jose import jwt

from app.config import settings


def test_with_no_user(client):
    response = client.post(
        "/token/", data={"username": "hello@gmail.com", "password": "hello"}
    )
    assert response.status_code == 404


def test_wrong_credentials(client, user_create):
    wrong_password = "hello123"
    response = client.post(
        "/token/", data={"username": user_create["email"], "password": wrong_password}
    )
    assert response.status_code == 401


def test_correct_credentials(client, user_create):
    response = client.post(
        "/token/",
        data={"username": user_create["email"], "password": user_create["password"]},
    )
    assert response.status_code == 200  # Not 201


def test_access_token(client, user_create):
    response = client.post(
        "/token/",
        data={"username": user_create["email"], "password": user_create["password"]},
    )
    payload = jwt.decode(
        response.json()["access_token"],
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )
    user_id = payload.get("sub")
    assert int(user_id) == user_create["user_id"]
    assert response.json()["token_type"] == "bearer"


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "hello", 404),
        ("hello@gmail.com", "wrongpassword", 401),
        ("wrongemail@gmail.com", "wrongpassword", 404),
        ("", "", 422),
        ("", "hello", 422),
        ("", "wrongpassword", 422),
        ("hello@gmail.com", "", 422),
        (None, None, 422),
    ],
)
def test_invalid_status(user_create, client, email, password, status_code):
    response = client.post("/token/", data={"username": email, "password": password})
    assert response.status_code == status_code
