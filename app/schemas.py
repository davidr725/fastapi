from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


# input model:
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# response model: response_model=UserOut
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


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
    created_at: datetime
    owner_id: int
    owner: UserOut


class PostOut(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    votes: int


class Token(BaseModel):
    access_token: str
    token_type: str


class Token_Data(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)
