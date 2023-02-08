from fastapi import APIRouter, Response, status, HTTPException
from pydantic import BaseModel, Field

class UserRequest(BaseModel):
    firstName: str
    lastName: str
    email: str
    password: str

class UserResponse(UserRequest):
    id: int | None = None

fake_db: list[UserResponse] = []


router = APIRouter()

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

@router.post("/registration", response_model=UserResponse | dict, response_model_exclude={"password"})
async def user_registration(user: UserRequest, response: Response):
    status_code = validate_registration(user)
    if status_code:
        raise HTTPException(status_code=400, detail="Invalid form fields")
    fake_db.append(user)
    id = fake_db.index(user)
    userout: UserResponse = UserResponse(
        id=id,
        firstName=user.firstName,
        lastName=user.lastName,
        email=user.email,
        password=user.password,
    )
    userout.id = id
    return userout

