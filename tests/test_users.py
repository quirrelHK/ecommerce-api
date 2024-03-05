import pytest
from jose import jwt
from app import schemas
from app.config import settings
    

    
       
    

def test_root(client):
    res = client.get("/")
    assert res.json().get("message") == "Hello There!"
    assert res.status_code == 200
    
def test_create_user(client):
    res = client.post(
        "/users/", 
        json={"email": "hello@gmail.com","password": "hello123"}
        )
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello@gmail.com"
    assert res.status_code == 201
    
def test_login_user(client, test_user):
    res = client.post(
        "/login", data={"username": test_user["email"], "password": test_user["password"]}
    )
    # print(res.json())
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200
    
@pytest.mark.parametrize("email, password, status_code",[
    ("wrongemail@gamil.com", "hello123", 403),
    ("hello@gamil.com", "wrongPassword", 403),
    ("wrongemail@gmail.com", "wrongPassword", 403),
    (None, "hello123", 422),
    ("hello@gamil.com", None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login",
                      data={"username": email, "password": password})
    
    assert res.status_code == status_code