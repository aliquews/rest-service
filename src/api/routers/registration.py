from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.accounts import UserCreate, UserReadContent
from src.db.database import get_async_session
from src.api.depend.accounts import validate_registration
from src.crud import account as user_crud



router = APIRouter(tags=["registration"])


@router.post("/registration")
async def register_user(
    user: UserCreate,
    session: AsyncSession = Depends(get_async_session),
):
    validate_registration(user)
    user.lastName = user.lastName.lower()
    user.firstName = user.firstName.lower()
    userDB = await user_crud.create(session=session, **user.dict())
    content = UserReadContent.from_orm(userDB)

    return content
