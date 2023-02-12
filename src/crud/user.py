import base64

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc, update, select
from fastapi import Depends

from src.db.database import get_async_session
from src.db.tables import User


async def create(session: AsyncSession, **kwargs):
    kwargs['password'] = base64.b64encode(kwargs['password'].encode()).decode('ascii')
    user = User(**kwargs)
    try:
        session.add(user)
    except exc.IntegrityError:
        return 409
    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise
    return user


async def update_user(id, session: AsyncSession, **kwargs):
    query = update(User).where(User.id == id).values(
        **kwargs).execution_options(synchronize_session='fetch')
    await session.execute(query)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise


async def get(id, session: AsyncSession):
    query = select(User).where(User.id == id)
    return list(await session.execute(query))[0]


async def get_many(session: AsyncSession, **kwargs):
    pass


async def delete(id, session: AsyncSession):
    query = session.delete(User).where(User.id == id)
    await session.execute(query)
    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    return None
