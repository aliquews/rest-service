from sqlalchemy import Table, Column, Integer, String
from db.database import metadata


user = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("FirstName", String, nullable=False),
    Column("LastName", String, nullable=False),
    Column("email", String, nullable=False),
    Column("password", String, nullable=False),
)
