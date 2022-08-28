from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.SqliteDb import Base


class SqliteUserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = relationship('SqliteEmailModel', back_populates='user', uselist=False)
    hashedPassword = relationship('SqlitePasswordHashModel', back_populates='user', uselist=False)

