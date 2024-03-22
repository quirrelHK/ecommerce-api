
from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"] # Used to group similar path operations together in FastAPI docs 
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut) # Default status code changed, first validate the pydantic model and only show that to the user (prevent sharing unneccesary data)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    
    if not db.query(models.User).filter(models.User.email == user.email).first() is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Username already exists.")
        
    hashed_password = utils.hash(user.password)
    user.password = hashed_password 
    new_user = models.User(**user.model_dump())
   
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    
    return user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), current_user: schemas.UserSession = Depends(oauth2.get_current_user)):
    
    user_query = db.query(models.User).filter(models.User.id == id)
    
    user = user_query.first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} was not found")
    
    if user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perfrom the requested action")
        
    user_query.delete(synchronize_session=False)
    db.commit()
 
    return Response(status_code=status.HTTP_204_NO_CONTENT)