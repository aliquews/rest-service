from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    first_name: str
    last_name: str
    email: str
    password: str # hashed password


class Users(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)


class UserCreate(UserBase):
    pass
