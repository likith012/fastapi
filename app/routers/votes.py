from fastapi import APIRouter, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from .. import schemas, models, oauth2, database


router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(vote: schemas.VoteCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id).filter(models.Vote.user_id == current_user.user_id)
    found_vote = vote_query.first()
    
    if vote.like:
        if found_vote is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You already voted this post")
        else:
            new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.user_id)
            db.add(new_vote)
            db.commit()
            return {"message": "Vote created"}
    else:
        if found_vote is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You didn't vote this post")
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message": "Vote deleted"}
        