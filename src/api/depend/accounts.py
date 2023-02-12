import base64
from fastapi import HTTPException, status, Header

from src.models.accounts import UserCreate


def validate_registration(user: UserCreate) -> None | int:
    props = [
        len(user.firstName.replace(" ", "")) if isinstance(user.firstName, str) else 0,
        len(user.lastName.replace(" ", "")) if isinstance(user.lastName, str) else 0,
        len(user.email.replace(" ", "")) if isinstance(user.email, str) else 0,
        len(user.password.replace(" ", "")) if isinstance(user.password, str) else 0,
    ]
    if not all(props):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid data",
        )
    return user

async def validate_id(accountid: int):
    if accountid is None or accountid <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="account id less than 0 or doesnt exists",
        )
    return accountid

 
def basic_auth(username, password):
    token = base64.b64encode(f"{username}:{password}".encode()).decode("ascii")
    return f'Basic {token}'

async def decode_auth(auth: str):
    token = auth.split()[1]
    decoded_auth = base64.b64decode(token).decode("ascii")
    return decoded_auth


async def get_current_user(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
        )
    return authorization