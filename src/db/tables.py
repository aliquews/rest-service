from sqlalchemy import Column, String, Integer, update
from .database import Base

# class User(SQLAlchemyBaseUserTable[int], Base):
#     pass

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
    
