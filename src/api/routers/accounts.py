import secrets
import base64
import json

from fastapi import APIRouter, Response, HTTPException, Depends, status, Header
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from sqlalchemy.ext.asyncio import AsyncSession


from src.models.accounts import UserCreate, UserReadContent
from src.api.depend.accounts import validate_registration, validate_id, basic_auth, get_current_user, decode_auth
from src.db.database import get_async_session

from src.crud import user as user_crud


router = APIRouter(tags=["Users"])
security = HTTPBasic()


@router.post("/registration")
async def register_user(
    user: UserCreate,
    response: Response,
    credentials: HTTPBasicCredentials = Depends(security),
    session: AsyncSession = Depends(get_async_session),
):
    validate_registration(user)
    userDB = await user_crud.create(session=session, **user.dict())
    content = UserReadContent.from_orm(userDB)

    token = basic_auth(user.email, user.password)
    response.headers['Authorization'] = token

    return content


@router.get("/accounts/search")
async def search_accounts(
    response: Response,
    credentials: HTTPBasicCredentials = Depends(security),
    firstName: str | None = None,
    lastName: str | None = None,
    email: str | None = None,
    from_: int = 0,
    size: int = 10,
    auth: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),

):
    if from_ < 0 or size <= 0:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    users = await user_crud.get_many(
        session=session,
        from_=from_,
        size=size,
        firstName=firstName,
        lastName=lastName,
        email=email,
    )
    if users == None:
        return []
    users = [UserReadContent.from_orm(user.User) for user in users]
    return users



@router.get("/accounts/{accountid}")
async def get_account_info(
    response: Response,
    credentials: HTTPBasicCredentials = Depends(security),
    accountid: int = Depends(validate_id),
    auth: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    user = await user_crud.get(accountid, session)

    userOut = UserReadContent.from_orm(user.User)
    print(await decode_auth(auth))
    return userOut

@router.put("/accounts/{accountid}")
async def update_acccount_info(
    response: Response,
    credentials: HTTPBasicCredentials = Depends(security),
    accountid: int = Depends(validate_id),
    user: UserCreate = Depends(validate_registration),
    auth: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),


):
    detect_user = await user_crud.get(accountid, session)
    detect_model = UserReadContent.from_orm(detect_user.User)
    decoded_auth = await decode_auth(auth)
    if detect_model.email != decoded_auth.split(":")[0]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    updated_user = await user_crud.update_user(accountid, session, **user.dict())
    userOut = UserReadContent.from_orm(updated_user.User)
    userAuth = UserCreate.from_orm(updated_user.User)
    token = basic_auth(userAuth.email, userAuth.password)
    return userOut