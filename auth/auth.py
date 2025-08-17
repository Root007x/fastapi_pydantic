from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from auth import models, schemas, security
from auth.db import get_db


oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

def get_user(db: Session, username :str):
    return db.query(models.User).filter(models.User.username == username).first()

async def get_current_user(
    token : str = Depends(oauth2_schema), db : Session = Depends(get_db)
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers = {"WWW-Authenticate" : "Bearer"}
    )
    try:
        payload = jwt.decode( # decode jwt token
            token,
            security.SECRET_KEY,
            algorithms=[security.ALGORITHM]
        )
        username : str = payload.get('sub')
        if username is None:
            raise credential_exception
        
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credential_exception
    
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credential_exception
    return user
