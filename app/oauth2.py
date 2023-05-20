from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from . import database, models, schemas
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict, expires_minutes: Optional[int] = None):
    to_encode = data.copy()

    if expires_minutes:
        expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    else:
        expire = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(access_token: str, credentials_exception):
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        token_data = schemas.TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(
    token_data: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token: str = verify_token(token_data, credentials_exception)
    user = db.query(models.User).filter(models.User.user_id == token.user_id).first()
    return user
