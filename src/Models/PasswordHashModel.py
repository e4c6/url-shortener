from pydantic import BaseModel


class PasswordHashModel(BaseModel):
    value: bytes

    def __str__(self) -> str:
        return str(self.value)

    def toJson(self):
        return self.toString()

    toString = __str__

    class Config:
        orm_mode = True
