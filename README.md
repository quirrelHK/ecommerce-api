# Back-end Clone of Social Media App Using FastAPI

The API and postgres database are deployed on render
[ecommerce-api-pqjs.onrender.com](https://ecommerce-api-pqjs.onrender.com/docs)

## This API has four routes

1. User route:\
    For creating new users and searching users by their id
2. Post route:\
    This route is used for creating, updating, deleting and checking posts.
3. Auth route:\
    Login system
4. Vote route:\
    This route is used for liking and disliking a post

## Clone this repo and cd into the folder
```
git clone https://github.com/quirrelHK/social-meida-app-api.git

cd social-meida-app-api
```

## Install the requirements
```
pip install -r requirements.txt
```

## You would require to set up your own database in postgre
Uncomment this line in main.py for creating tables using sqlalchemy
```py
models.Base.metadata.create_all(bind=engine)
```
Or you can use alembic for creating tables.

After this create a .env file in the current directory and add the following:
```
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=your_db_password
DATABASE_NAME=your_db_name
DATABASE_USERNAME=your_db_user_name
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

You can generate secret key using this command in terminal:
```
openssl rand -hex 20
```
## Run the app
```
uvicorn app.main:app --reload
```


## Alternatively you can use docker
You call pull the image from docker-hub:
```
docker pull ritesh778/apipython

```
Or build the and run the image:
```
docker-compose -f docker-compose-dev.yml up -d --build

```

