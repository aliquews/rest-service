
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from src.models.locations import LocationCreate, LocationRead
from src.api.depend.auth import auth_basic
from src.api.depend.accounts import validate_id
from src.db.database import get_async_session
from src.crud import location as crud


router = APIRouter(
    tags=["locations"],
    dependencies=[Depends(auth_basic)], 
)

@router.post("/locations")
async def create_location(
    location: LocationCreate,
    session: AsyncSession = Depends(get_async_session),
):
    locDB = await crud.create_(session, **location.dict())
    locOut = LocationRead.from_orm(locDB)
    return locOut

@router.get("/locations/{pointid}")
async def get_location_info(
    pointid: int = Depends(validate_id),
    session: AsyncSession = Depends(get_async_session),
    
):
    locDB = await crud.get_(pointid, session)
    locOut = LocationRead.from_orm(locDB.Location)
    return locOut

@router.put("/locations/{pointid}")
async def update_location_info(
    pointid: int = Depends(validate_id),
    session: AsyncSession = Depends(get_async_session),
):
    point = await crud.update_(id=pointid, session=session)
    locOut = LocationRead.from_orm(point.Location)
    return locOut

@router.delete("/locations/{pointid}")
async def delete_location(
    pointid: int = Depends(validate_id),
    session: AsyncSession = Depends(get_async_session),
):
    await crud.delete_(id=pointid, session=session)
    return