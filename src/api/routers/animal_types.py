from fastapi import APIRouter, Depends

from src.api.depend.auth import auth_basic
from src.models.types import TypeCreate, TypeRead


router = APIRouter(
    tags=["Animal Types"],
    dependencies=[Depends(auth_basic), ],
)


@router.get("/animals/types{typeid}")
async def get_type(typeid: int):
    pass

@router.post("/animals/types")
async def create_type(type:TypeCreate):
    pass

@router.put("/animals/types{typeid}")
async def update_type(typeid: int, type: TypeCreate):
    pass

@router.delete("/animals/types/{typeid}")
async def delete_type(typeid: int):
    pass