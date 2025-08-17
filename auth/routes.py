from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth import auth, models, schemas, security
from auth.db import get_db


router = APIRouter()


@router.post("/register/", response_model=schemas.UserInDBBase)
async def register(user_in : schemas.UserIn, db : Session = Depends(get_db)):
    
    db_user = auth.get_user(db, username = user_in.username)
    
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db_user = db.query(models.User).filter(models.User.email == user_in.email).first()
    
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = security.get_password_hash(user_in.password)
    
    db_user = models.User(
        **user_in.model_dump(exclude={"password"}),
        hashed_password = hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)
):
    user = auth.get_user(db, username=form_data.username)
    
    if not user or not security.pwd_context.verify(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers = {"WWW-Authenticate" : "Bearer"}
        )
        
    access_token_expire = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE)
    
    access_token = security.create_access_token(
        data = {'sub' : user.username},
        expires_delta=access_token_expire
    )
    
    return {"access_token" : access_token, "token_type" : "bearer"}


@router.get("/conv")
async def read_conv(
    current_user : schemas.UserInDB = Depends(auth.get_current_user)
):
    print(f"Accessed with token for user: {current_user.username}")
    return {"Role" : "Hello Boss", "Current_user" : current_user.username}
    
        
    
    
    