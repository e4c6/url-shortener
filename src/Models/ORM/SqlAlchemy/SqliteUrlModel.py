from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.SqliteDb import Base


class SqliteUrlModel(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True)
    value = Column(String)
    urlKeyId = Column(Integer, ForeignKey('url_keys.id'))
    urlKey = relationship('SqliteUrlKeyModel', back_populates='url')

