from fastapi import APIRouter, HTTPException, status, Depends, Response
from typing import List
from sqlalchemy.orm import Session
import models
import database
from database import get_db
import schemas
from schemas import PostCreate
import oauth2
from typing import Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):
    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .filter(models.Post.title.contains(search))
        .group_by(models.Post.id)
        .limit(limit)
        .offset(skip)
        .all()
    )

    results = []
    for post, votes in posts:
        results.append({"Post": post, "votes": votes})

    return results











@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: PostCreate, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    print(f"Creating post for user_id: {current_user.id}")  # Add logging
    try:
        new_post = models.Post(**post.dict(), user_id=int(current_user.id))
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    except Exception as e:
        print(f"Error while creating post: {str(e)}")  # Add logging for error
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    
    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.user_id !=current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this post")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: PostCreate, db: Session = Depends(get_db),current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this post")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
