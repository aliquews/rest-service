from typing import Optional
from pydantic import BaseModel


class Headers(BaseModel):
    Authorization: str

class UserCreate(BaseModel):
    firstName: str
    lastName: str
    email: str
    password: str



class UserReadContent(BaseModel):
    id: int
    firstName: str
    lastName: str
    email: str

    class Config:
        orm_mode = True


class UserRead(BaseModel):
    headers: Headers
    content: UserReadContent
