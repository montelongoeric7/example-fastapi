from fastapi import APIRouter, HTTPException, Response, status, Depends
from typing import Optional, List
from sqlalchemy.orm import Session
import database
from database import get_db
import schemas
from schemas import UserLogin
import models
import utils
import oauth2
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags = ["Authentication"]
)


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm= Depends(),db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=403, detail="User not found")

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=403, detail="Invalid credentials")
    
    access_token = oauth2.create_access_token(data={"user_id":user.id})
    
    #cretae a token and return token
    return {"access_token": access_token, "token_type": "bearer"}