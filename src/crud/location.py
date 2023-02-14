import base64

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc, update, select, delete
from fastapi import HTTPException, status

from src.db.tables import Location


async def get_(id: int, session: AsyncSession):
    query = select(Location).where(Location.id == id)
    result = list(await session.execute(query))

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found",
        )
    return result[0]

async def create_(session: AsyncSession, **kwargs):
    location = Location(**kwargs)
    session.add(location)

    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Location is already exists",
        )
    return location

async def update_(id: int, session: AsyncSession, **kwargs):
    try:
        query = update(Location).where(Location.id == id).values(**kwargs).execution_options(synchronize_session='fetch')
        await session.execute(query)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
    try:
        await session.commit()
        return await get_(id=id, session=session)
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

async def delete_(id: int, session: AsyncSession):
    query = delete(Location).where(Location.id == id)
    try:
        await session.execute(query)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = str(e),
        )
    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )