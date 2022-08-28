from __future__ import annotations
from pydantic import BaseModel
from src.Models.EmailModel import EmailModel
from src.Models.PasswordHashModel import PasswordHashModel


class UserModel(BaseModel):
    email: EmailModel
    hashedPassword: PasswordHashModel

    def toJson(self) -> dict:
        return {
            'email': self.email.toString(),
            'password': self.hashedPassword.toString(),
        }

    def compareCredentials(self, target: UserModel) -> bool:
        passwordMatch: bool = self.hashedPassword.toString() == target.hashedPassword.toString()
        emailMatch: bool = self.email.toString() == target.email.toString()

        return passwordMatch and emailMatch

    class Config:
        orm_mode = True


