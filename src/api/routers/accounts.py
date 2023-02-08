from typing import List
from fastapi import APIRouter, Response, status, HTTPException, Query
from pydantic import BaseModel, Field

class UserRequest(BaseModel):
    firstName: str
    lastName: str
    email: str
    password: str

class UserDB(UserRequest):
    id: int | None = None

class UserResponse(BaseModel):
    id: int | None
    firstName: str
    lastName: str
    email: str

fake_db: list[UserDB] = []


router = APIRouter(tags=["Users"])

def validate_registration(user: UserRequest) -> None | int:
    props = [
        len(user.firstName.replace(" ", "")) if isinstance(user.firstName, str) else 0,
        len(user.lastName.replace(" ", "")) if isinstance(user.lastName, str) else 0,
        len(user.email.replace(" ", "")) if isinstance(user.email, str) else 0,
        len(user.password.replace(" ", "")) if isinstance(user.password, str) else 0,
    ]
    if not all(props):
        return 400
    return None

@router.post("/registration", response_model=UserResponse | dict)
async def user_registration(user: UserRequest, response: Response):
    status_code = validate_registration(user)
    if status_code:
        raise HTTPException(status_code=400, detail="Invalid form fields")
    fake_db.append(user)
    id = fake_db.index(user)
    userout: UserDB = UserDB(
        id=id,
        firstName=user.firstName,
        lastName=user.lastName,
        email=user.email,
        password=user.password,
    )
    fake_db.pop(id)
    fake_db.append(userout)
    return userout


@router.get("/accounts/{accountid}", response_model= UserResponse)
async def get_user_info(accountid: int):
    return fake_db[accountid]


@router.get("/accounts/search", response_model=List[UserResponse])
async def get_user_by_query(
    firstName: str,
    lastName: str,
    email: str,
    _from: int,
    size: int,
):
    pass

@router.put("/accounts/{accountid}", response_model=UserResponse)
async def update_user_info(accountid: int, user: UserRequest):
    status_code = validate_registration(user)
    if status_code:
        raise HTTPException(status_code=400, detail="Invalid form fields")
    userout: UserDB = UserDB(
        id=accountid,
        firstName=user.firstName,
        lastName=user.lastName,
        email=user.email,
        password=user.password,
    )
    fake_db[accountid] = userout
    return userout


@router.delete("/accounts/{accountid}")
async def delete_user(accountid: int):
    fake_db.pop(accountid)
