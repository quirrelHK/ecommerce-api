from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# request; Get method, url: /posts
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user), 
              limit: int = 10, skip: int = 0, search: Optional[str] = ""): # Using orm you need this session object wheneve you want to access the DB
    

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, 
        models.Vote.post_id == models.Post.id, 
        isouter=True
        ).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts   # FastAPI will automatically serialise this list into a Json


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) # Default status code changed, first validate the pydantic model and only show that to the user (prevent sharing unneccesary data)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)): # Extract all the fields from body and convert the python dictionary
    '''
    Structure of data we expect; title str, content str
    '''
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.model_dump(), owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # Retreiving the post we created
    
    return new_post

# Fetch a single post
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):   # FastAPI will automatically convert it to an integer; also validate the field, if it can be converted

    # post = db.query(models.Post).filter(models.Post.id == id).first() # Find first instance and return that, save resources

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, 
        models.Vote.post_id == models.Post.id, 
        isouter=True
        ).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perfrom requested action")
        
    post_query.delete(synchronize_session=False)
    db.commit()
    # When you delete something and send status code 204, you don't want to return anything back
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update all fields
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    original_post = post_query.first()
    if original_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    

    if original_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()