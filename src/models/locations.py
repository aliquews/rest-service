from pydantic import BaseModel


class LocationRead(BaseModel):
    id: int
    latitude: float
    longitude: float

    class Config:
        orm_mode = True


class LocationCreate(BaseModel):
    latitude: float
    longitude: float

    class Config:
        orm_mode = True