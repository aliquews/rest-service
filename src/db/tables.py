from sqlalchemy import Column, String, Integer, BigInteger, Float
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    firstName = Column(String)
    lastName = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"email={self.email}, "
            f")>"
        )
    

class Location(Base):
    __tablename__ = "locations"
    id = Column(BigInteger,primary_key=True, autoincrement=True)
    latitude = Column(Float)
    longitude = Column(Float)
    uniq_coord = Column(BigInteger, unique=True)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}(lat={self.latitude}, lon={self.longitude})>'