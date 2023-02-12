from .accounts import router as acc_router
from .animals import router as animal_router
from fastapi import APIRouter


router = APIRouter()

router.include_router(acc_router)
router.include_router(animal_router)