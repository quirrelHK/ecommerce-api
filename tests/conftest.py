# All the fixture in this file can be access by all test modules in the folder
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

# Engine connects sqlalchemy to postgres database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
# app.dependency_overrides[get_db] = override_get_db
# client = TestClient(app)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
 
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    
    # Run our code before we run our test
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    # Run our code after the test finished
 
# Create a different user; used for testing creating posts, now database will have posts by two users
# For testing if an authorized user can update or delete another's post
@pytest.fixture
def test_user2(client):
    user_data = {
        "email": "hello1@gamil.com",
        "password": "hello123"
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user 
   
@pytest.fixture
def test_user(client):
    user_data = {
        "email": "hello@gamil.com",
        "password": "hello123"
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user 



@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user["id"]
    },{
        "title": "second title",
        "content": "second content",
        "owner_id": test_user["id"]
    },{
        "title": "third title",
        "content": "third content",
        "owner_id": test_user["id"]        
    },{
        "title": "fourth title",
        "content": "fourth content",
        "owner_id": test_user2["id"]        
    }]
    
    def create_post_model(post):
        return models.Post(**post)
    
    posts_data = list(map(create_post_model, posts_data))
    session.add_all(posts_data)
    session.commit()
    
    posts = session.query(models.Post).all()
    return posts