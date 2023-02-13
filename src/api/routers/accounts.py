import secrets
import base64
import json

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBasicCredentials

from sqlalchemy.ext.asyncio import AsyncSession


from src.models.accounts import UserCreate, UserReadContent
from src.api.depend.accounts import validate_registration, validate_id, validate_change_user
from src.api.depend.auth import auth_basic
from src.db.database import get_async_session

from crud import account as user_crud


router = APIRouter(
    tags=["Users"],
    dependencies=[Depends(auth_basic)],    
)


@router.get("/accounts/search")
async def search_accounts(
    firstName: str | None = None,
    lastName: str | None = None,
    email: str | None = None,
    from_: int = 0,
    size: int = 10,
    session: AsyncSession = Depends(get_async_session),

):
    
    firstName = firstName.lower() if isinstance(firstName, str) else None
    lastName = lastName.lower() if isinstance(lastName, str) else None
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
    accountid: int = Depends(validate_id),
    session: AsyncSession = Depends(get_async_session)
):
    user = await user_crud.get(session, id=accountid)
    userOut = UserReadContent.from_orm(user.User)
    return userOut


@router.put("/accounts/{accountid}")
async def update_acccount_info(
    accountid: int = Depends(validate_id),
    user: UserCreate = Depends(validate_registration),
    #auth: HTTPBasicCredentials = Depends(auth_basic),
    session: AsyncSession = Depends(get_async_session),


):
    await validate_change_user(*router.dependencies, accountid, session)
    updated_user = await user_crud.update_user(accountid, session, **user.dict())
    userOut = UserReadContent.from_orm(updated_user.User)
    return userOut


@router.delete("/accounts/{accountid}")
async def delete_account(
    accountid: int,
    auth: HTTPBasicCredentials = Depends(auth_basic),
    session: AsyncSession = Depends(get_async_session),
):
    await validate_change_user(auth, accountid, session)

    await user_crud.delete_(accountid, session)

    return 