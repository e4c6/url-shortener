from pydantic import BaseModel


class EmailModel(BaseModel):
    value: str

    def __str__(self) -> str:
        return self.value

    def toJson(self):
        return self.value

    toString = __str__

    class Config:
        orm_mode = True
