from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, models, oauth2, schemas, utils

router = APIRouter(tags=["Auth"])


@router.post(
    "/token/", response_model=schemas.AccessToken, status_code=status.HTTP_200_OK
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User with email not found"
        )

    verify: bool = utils.verify_hash(form_data.password, user.password)

    if not verify:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = oauth2.create_access_token(data={"sub": str(user.user_id)})
    return {"access_token": access_token, "token_type": "bearer"}
