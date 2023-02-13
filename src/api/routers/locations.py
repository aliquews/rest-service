from fastapi import APIRouter, Depends


router = APIRouter(
    tags=["locations"],
    dependencies=[Depends()],    
)


@router.get("/locations/{pointid}")
async def get_location_info(
    pointid: int,
    
):
    pass