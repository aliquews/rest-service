from .accounts import router as acc_router
from fastapi import APIRouter

router = APIRouter()
router.include_router(acc_router)