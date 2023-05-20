from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=List[schemas.ResponseOut]
)
def get_posts(
    limit: Union[int, None] = None,
    skip: int = 0,
    search: Union[str, None] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    posts_with_votes = (
        db.query(models.Post, func.count(models.Vote.post_id).label("Likes"))
        .outerjoin(models.Vote, models.Vote.post_id == models.Post.post_id)
        .group_by(models.Post.post_id)
    )

    if search is None:
        getall_posts = posts_with_votes.filter(
            models.Post.owner_id == current_user.user_id
        )
    else:
        getall_posts = posts_with_votes.filter(
            models.Post.owner_id == current_user.user_id
        ).filter(models.Post.content.contains(search))

    if limit is None:
        getall_posts = getall_posts.offset(skip).all()
    else:
        getall_posts = getall_posts.limit(limit).offset(skip).all()

    return getall_posts


@router.get(
    "/{id}/", status_code=status.HTTP_200_OK, response_model=schemas.ResponseOut
)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    posts_with_votes = (
        db.query(models.Post, func.count(models.Vote.post_id).label("Likes"))
        .outerjoin(models.Vote, models.Vote.post_id == models.Post.post_id)
        .group_by(models.Post.post_id)
    )
    get_post_id = posts_with_votes.filter(models.Post.post_id == id).first()

    if get_post_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )

    return get_post_id


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseBase
)
def create_post(
    post: schemas.RequestCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    new_post = models.Post(owner_id=current_user.user_id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    del_post = db.query(models.Post).filter(models.Post.post_id == id)

    if del_post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )

    if del_post.first().owner_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this post",
        )

    del_post.delete(synchronize_session=False)
    db.commit()
    return


@router.put(
    "/{id}/", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ResponseBase
)
def update_post(
    id: int,
    post: schemas.RequestUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    update_post = db.query(models.Post).filter(models.Post.post_id == id)

    if update_post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )

    if update_post.first().owner_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this post",
        )

    update_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return update_post.first()
