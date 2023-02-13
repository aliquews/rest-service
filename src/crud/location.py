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
    pass

async def update_(session: AsyncSession, **kwargs):
    pass

async def delete_(id: int, session: AsyncSession):
    pass