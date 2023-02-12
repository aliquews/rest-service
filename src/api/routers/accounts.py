import secrets
import base64
import json

from fastapi import APIRouter, Response, HTTPException, Depends, status, Header
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from sqlalchemy.ext.asyncio import AsyncSession


from src.models.accounts import UserCreate, UserReadContent
from src.api.depend.accounts import validate_registration
from src.db.database import get_async_session

from src.crud import user as user_crud



router = APIRouter(tags=["Users"])
security = HTTPBasic()


def basic_auth(username, password):
    token = base64.b64encode(f"{username}:{password}".encode()).decode("ascii")
    return f'Basic {token}'



async def get_current_user(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
        )
    return authorization


@router.post("/registration", response_model=UserReadContent)
async def register_user(
    user: UserCreate,
    response: Response,
    credentials: HTTPBasicCredentials = Depends(security),
    session: AsyncSession = Depends(get_async_session),
):
    if validate_registration(user):
        return HTTPException(
            status_code=400,
            detail="Incorrect input data",
        )
    userDB = await user_crud.create(session=session,**user.dict())
    content = UserReadContent.from_orm(userDB)

    token = basic_auth(user.email, user.password)
    response.headers['Authorization'] = token

    return content


@router.get("/accounts/{accountid}", response_model=UserReadContent)
async def get_account_info(accountid: int, auth: str = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    user = await user_crud.get(accountid, session)
    
    userOut = UserReadContent.from_orm(user.User)
    return userOut