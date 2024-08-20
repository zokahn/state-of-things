
from typing import List, Optional
from pydantic import BaseModel

class TokenData(BaseModel):
    username: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    projects: List[str] = []

    class Config:
        orm_mode = True

# Add your existing project-related schemas here
