import os

from sqlmodel import create_engine, SQLModel, Session

from config import DB_URL


engine = create_engine(DB_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

