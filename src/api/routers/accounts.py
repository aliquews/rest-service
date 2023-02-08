from fastapi import APIRouter


router = APIRouter(tags=["Accounts"])


@router.get("/accounts")
async def account_list():
    """
    API endpoint, that gets accounts list (TEST)
    """
    return {"accounts": []}