from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from app.database import Base

#Schema/Pydantic model, provides the structure of a request & response
#ensures that the request and response are shaped in a specific way
# pydantic model != model saved in models 

class UserBase(BaseModel):
    email: EmailStr
    password: str
    
class UserCreate(UserBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        from_attributes = True
        

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True 
    
class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    owner_id : int
    created_at: datetime
    owner: UserOut
    
    class Config:
        from_attributes = True
        
class PostOut(BaseModel):
    Post: Post
    votes: int
    
    class Config:
        from_attributes = True
        

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: str | None
    
class Vote(BaseModel):
    post_id: int
    dir: int