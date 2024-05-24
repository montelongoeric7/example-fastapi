from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
import models
import database
import schemas
import oauth2
import logging

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

logging.basicConfig(level=logging.INFO)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    try:
        post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
        found_vote = vote_query.first()

        if vote.dir == 1:
            if found_vote:
                raise HTTPException(status_code=400, detail="You have already upvoted this post")
            new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
            db.add(new_vote)
            db.commit()
            return {"message": "Upvoted successfully"}
        else:
            if not found_vote:
                raise HTTPException(status_code=400, detail="You have not upvoted this post")
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message": "Successfully deleted vote"}
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


