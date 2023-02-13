import base64

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_async_session
from crud import account as user_crud
from src.models.accounts import UserCreate


security = HTTPBasic()


async def auth_basic(credentials: HTTPBasicCredentials = Depends(security), session: AsyncSession = Depends(get_async_session)):
    print(credentials.username, credentials.password)
    try:
        user = await user_crud.get(session, email=credentials.username)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    userModel = UserCreate.from_orm(user.User)
    hashed_pass = base64.b64encode(credentials.password.encode()).decode('ascii')
    if userModel.email != credentials.username or userModel.password != hashed_pass:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    return credentials