import base64

from fastapi import FastAPI, HTTPException
from src.api.routers import router

app = FastAPI()

@app.middleware("http")
async def update_authorization_header(request, call_next):
    response = await call_next(request)

    if request.url.path == "/accounts" and request.method == "PUT":
        authorization = request.headers.get("Authorization")
        if authorization is None:
            raise HTTPException(status_code=400, detail="Authorization header not found")

        try:
            scheme, credentials = authorization.split()
            if scheme.lower() != 'basic':
                raise HTTPException(status_code=400, detail="Invalid Authorization header")
            decoded_credentials = base64.b64decode(credentials).decode()
            email, password = decoded_credentials.split(':')
        except (ValueError, TypeError):
            raise HTTPException(status_code=400, detail="Invalid Authorization header")


        updated_credentials = f"{email}:{password}"
        encoded_credentials = base64.b64encode(updated_credentials.encode()).decode()
        response.headers["Authorization"] = f"Basic {encoded_credentials}"

    return response


@app.on_event("startup")
async def info_logging():
    pass


app.include_router(router)
