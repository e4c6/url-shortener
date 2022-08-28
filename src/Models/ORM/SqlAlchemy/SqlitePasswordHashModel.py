from sqlalchemy import Column, Integer, String, ForeignKey, BLOB
from sqlalchemy.orm import relationship

from src.Models.PasswordHashModel import PasswordHashModel
from src.SqliteDb import Base


class SqlitePasswordHashModel(Base):
    __tablename__ = 'passwords'
    id = Column(Integer, primary_key=True)
    value = Column(BLOB)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('SqliteUserModel', back_populates='hashedPassword')

    @staticmethod
    def from_base(basePassword: PasswordHashModel):
        return SqlitePasswordHashModel(value=basePassword.value)




