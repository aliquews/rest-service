from fastapi import APIRouter


router = APIRouter(tags=["Animals"])


@router.get("/animals/{animalid}")
async def get_animal_info(animalid: int):
    pass


@router.get("/animals/search")
async def search_animal():
    pass


@router.get("/animals/types/{typeid}")
async def show_type_info():
    pass


@router.get("/locations/{pointid}")
async def show_location_info():
    pass


@router.get("/animals/{animalid}/locations")
async def get_moving_info():
    pass