from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import engine, get_db
from ..schemas import UserCreate, UserOut
from sqlalchemy.orm import Session


router = APIRouter(prefix="/users", tags=["Users"])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_users(user: UserCreate, db: Session = Depends(get_db)):
    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(
        **user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # retrieve and store back in new post

    return new_user


@router.get('/{id}', response_model=UserOut)
# : int is validation by fastapi, ensures automatic error handling
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} does not exist")

    return user
