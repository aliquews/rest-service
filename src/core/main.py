from fastapi import FastAPI
from src.api.routers import router

app = FastAPI()


@app.on_event("startup")
async def info_logging():
    pass


app.include_router(router)
