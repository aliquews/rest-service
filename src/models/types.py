from pydantic import BaseModel


class TypeCreate(BaseModel):
    type: str

class TypeRead(BaseModel):
    id: int
    type: str