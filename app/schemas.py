from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        from_attributes = True
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class UserSession(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    
# Schema of the data we expect, Does the validation
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # (optional value) If the post should be published or not
    
    
class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    # Pydantic expects a post of type dict, it does not know what to do with sqlalchemy object, so this class is required
    class Config:
        from_attributes = True
        
class PostOut(BaseModel):
    Post: Post
    votes: int
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[int] = None
    
class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1) # Only ollow direction of 0(remove like) and direction of 1(like) 