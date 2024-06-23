from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import user, post, auth, vote



# Create the table, if table already exists then sqlalchemy does not touch it (for DB initialization you would want to use Alembic)
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = []

# Allows our API to talk to different domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include all the routes
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



# Path Operation
@app.get("/") # Path operation decorator
def root(): # Path operation function
    
    return {"message": "Hello There!"}
 


