import base64

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc, update, select
from fastapi import HTTPException, status

from src.db.database import get_async_session
from src.db.tables import User


async def create(session: AsyncSession, **kwargs):
    kwargs['password'] = base64.b64encode(
        kwargs['password'].encode()).decode('ascii')
    user = User(**kwargs)
    session.add(user)
    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise
    return user


async def update_user(id, session: AsyncSession, **kwargs):
    try:
        kwargs['password'] = base64.b64encode(
        kwargs['password'].encode()).decode('ascii')
    except:
        pass
    try:
        query = update(User).where(User.id == id).values(
            **kwargs).execution_options(synchronize_session='fetch')
        result = await session.execute(query)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    try:
        await session.commit()
        return await get(id, session)
    except [Exception, exc.IntegrityError]:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        )


async def get(id, session: AsyncSession):
    query = select(User).where(User.id == id)
    result = list(await session.execute(query))
    if len(result) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return result[0]


async def get_many(session: AsyncSession, from_: int, size: int, **kwargs):
    query = select(User)
    for key in kwargs.keys():
        if kwargs[key] == None:
            continue
        query = query.where(User.__dict__[key] == kwargs[key])
    result = list(await session.execute(query))
    if len(result[from_:]) < size:
        return result[from_:]
    return result[from_:size]


async def delete(id, session: AsyncSession):
    query = session.delete(User).where(User.id == id)
    await session.execute(query)
    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    return None
