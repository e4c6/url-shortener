from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.Models.EmailModel import EmailModel
from src.SqliteDb import Base


class SqliteEmailModel(Base):
    __tablename__ = 'emails'
    id = Column(Integer, primary_key=True)
    value = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('SqliteUserModel', back_populates='email')

    @staticmethod
    def from_base(baseEmail: EmailModel):
        return SqliteEmailModel(value=baseEmail.value)
