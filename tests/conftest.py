from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import pytest

from app.config import settings
from app.main import app
from app.models import Base
from app.database import get_db
from app.oauth2 import create_access_token
from app import models


SQLALCHEMY_DATABASE_URL = f"{settings.DATABASE_TYPE}://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Fixtures for users endpoints
@pytest.fixture
def session():
    Base.metadata.create_all(bind=engine) # create tables
    
    test_db = TestingSessionLocal()
    try:
        yield test_db
    finally:
        test_db.close()
        
    Base.metadata.drop_all(bind=engine) # drop tables

@pytest.fixture
def client(session):    
    # Dependency function for overriding get_db
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
            
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c


# Fixture for auth endpoints
@pytest.fixture
def user_create(client):
    response = client.post("/users/", json={"username": "hello", "password": "hello", "email": "hello@gmail.com"})
    assert response.status_code == 201
    user_with_passwd = response.json()
    user_with_passwd["password"] = "hello"
    return user_with_passwd


# Fixture for posts endpoints
@pytest.fixture
def access_token(user_create):
    return create_access_token({'sub': str(user_create['user_id'])})

@pytest.fixture
def authorized_client(access_token, client):
    client.headers["Authorization"] = f"Bearer {access_token}"
    return client

@pytest.fixture
def post_create(user_create, session):
    posts_data = [
        {
        "title": "Hello",
        "content": "Hello World!",
        "published": True,
        "owner_id": user_create['user_id']
        },
        {"title": "Hello2",
        "content": "Hello World2!",
        "published": True,
        "owner_id": user_create['user_id']
        },
        {"title": "Hello3",
        "content": "Hello World3!",
        "published": True,
        "owner_id": user_create['user_id']
        }
    ]
        
    session.add_all([models.Post(**post) for post in posts_data])
    session.commit()
    posts = session.query(models.Post).all()
    return posts
    

# Fixtures for votes endpoints
@pytest.fixture
def like_create(user_create, post_create, session):
    like_data = {
        "user_id": user_create['user_id'],
        "post_id": post_create[0].post_id
    }
    session.add(models.Vote(**like_data))
    session.commit()
    likes = session.query(models.Vote).filter(models.Vote.post_id == post_create[0].post_id).filter(models.Vote.user_id == user_create['user_id']).first()
    print(likes)
    return likes
