from sqlalchemy import Column
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Integer, String

# Create database table

from auth.db import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key = True, index = True)
    username = Column(String, unique=True, index = True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

