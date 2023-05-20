from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, utils
from ..database import get_db


router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=List[schemas.UserGetOut]
)
def get_user(limit: int = -1, skip: int = 0, db: Session = Depends(get_db)):
    if limit == -1:
        getall_users = db.query(models.User).offset(skip).all()
    else:
        getall_users = db.query(models.User).limit(limit).offset(skip).all()
    return getall_users


@router.get("/{id}/", status_code=status.HTTP_200_OK, response_model=schemas.UserGetOut)
def get_user(id: int, db: Session = Depends(get_db)):
    get_user_id = db.query(models.User).filter(models.User.user_id == id).first()

    if get_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
        )

    return get_user_id


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreateOut
)
def create_user(user: schemas.UserCreateIn, db: Session = Depends(get_db)):
    db_email = db.query(models.User).filter(models.User.email == user.email).first()

    if db_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
