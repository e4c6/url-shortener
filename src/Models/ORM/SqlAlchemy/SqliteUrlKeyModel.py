from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.SqliteDb import Base


class SqliteUrlKeyModel(Base):
    __tablename__ = 'url_keys'
    id = Column(Integer, primary_key=True)
    key = Column(String)
    url = relationship('SqliteUrlModel', back_populates='urlKey', uselist=False)
