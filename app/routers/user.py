from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
import models
import database
from database import engine, get_db
import schemas
from schemas import PostCreate, UserCreate
from utils import pwd_context, hash_password

router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id:int, db:Session = Depends(get_db)):
    user= db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
    