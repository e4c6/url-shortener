from src.Models.UrlModel import UrlModel
from pydantic import BaseModel


class UrlKeyModel(BaseModel):
    key: str
    targetUrl: UrlModel

    def __str__(self) -> str:
        return self.key

    def toJson(self):
        return {'key': self.key, 'targetUrl': self.targetUrl}

    toString = __str__

    def toPath(self):
        return '/' + self.toString()

    class Config:
        orm_mode = True
