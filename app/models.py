from datetime import datetime

from pydantic import BaseModel


class ImageInbox(BaseModel):
    id: int
    frame_id: int
    name: str
    created_at: datetime

    class Config:
        orm_mode = True


class ImageGet(ImageInbox):
    content: bytes


class BaseUser(BaseModel):
    login: str


class UserCreate(BaseUser):
    password: str


class User(BaseUser):
    id: int
    password_hash: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
