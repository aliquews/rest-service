from .accounts import router as acc_router
from .animals import router as animal_router
from .registration import router as reg_router
from .locations import router as loc_router
from fastapi import APIRouter


router = APIRouter()

router.include_router(reg_router)
router.include_router(acc_router)
router.include_router(loc_router)
#router.include_router(animal_router)