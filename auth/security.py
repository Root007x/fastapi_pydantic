from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from passlib.context import CryptContext


# openssl rand -hex 32
SECRET_KEY = "d6b7e971eebd5bebb6afededb2b1c2526598cdd9b89f108083733c444077edbe"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = 30 * 24 * 60 # 30 days

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

# get hash password
def get_password_hash(password : str):
    return pwd_context.hash(password)

# Create access token
def create_access_token(data: dict, expires_delta : Optional[timedelta] = None):
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
        
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({
        "exp" : expire
    })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # create token
    return encoded_jwt