from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import sessionmaker

from src.Adapters.IDbAdapter import IDbAdapter
from src.Exceptions.EmptyUserInformationError import EmptyUserInformationError
from src.Exceptions.UrlNotFoundError import UrlNotFoundError
from src.Models.EmailModel import EmailModel
from src.Models.ORM.SqlAlchemy.SqliteEmailModel import SqliteEmailModel
from src.Models.ORM.SqlAlchemy.SqlitePasswordHashModel import SqlitePasswordHashModel
from src.Models.ORM.SqlAlchemy.SqliteUrlKeyModel import SqliteUrlKeyModel
from src.Models.ORM.SqlAlchemy.SqliteUrlModel import SqliteUrlModel
from src.Models.ORM.SqlAlchemy.SqliteUserModel import SqliteUserModel
from src.Models.UrlKeyModel import UrlKeyModel
from src.Models.UrlModel import UrlModel
from src.Models.UserModel import UserModel
from src.Models.UserModelFactory import UserModelFactory


class SqliteAdapter(IDbAdapter):
    passwordSalt: str = None
    db: sessionmaker = None

    def __init__(self, dbClient: sessionmaker, passwordSalt: str):
        self.passwordSalt = passwordSalt
        self.db = dbClient

    def resolveShortUrl(self, shortUrl: UrlKeyModel) -> UrlModel:
        with self.db.begin() as session:
            urlKey = session.query(SqliteUrlKeyModel).filter(SqliteUrlKeyModel.key == shortUrl.key).first()
            if not urlKey:
                raise UrlNotFoundError
            urlOrm = session.query(SqliteUrlModel).filter(SqliteUrlModel.urlKeyId == urlKey.id).first()
            if not urlOrm:
                raise UrlNotFoundError
            url = UrlModel.from_orm(urlOrm)
            return url

    def getUser(self, email: EmailModel) -> UserModel:
        with self.db.begin() as session:
            email_orm: SqliteEmailModel = session.query(SqliteEmailModel).filter(SqliteEmailModel.value == email.value).first()
            user_orm: SqliteUserModel = session.get(SqliteUserModel, email_orm.user_id)
            if not user_orm:
                raise EmptyUserInformationError

            user = UserModelFactory(self.passwordSalt).fromDict(
                {
                    'email': user_orm.email.value,
                    'password': user_orm.hashedPassword.value
                }
            )
            return user

    def putShortUrl(self, shortUrl: UrlKeyModel) -> None:
        with self.db.begin() as session:
            url = SqliteUrlKeyModel(key=shortUrl.key, url=SqliteUrlModel(value=shortUrl.targetUrl.value))
            session.add(url)
        return

    def putUser(self, user: UserModel) -> None:
        with self.db.begin() as session:
            password = SqlitePasswordHashModel.from_base(user.hashedPassword)
            email = SqliteEmailModel.from_base(user.email)
            user = SqliteUserModel(email=email, hashedPassword=password)
            session.add(user)
        return

    def authorizeUser(self, loginAttemptCredentials: UserModel) -> bool:
        with self.db.begin() as session:
            user = self.getUser(loginAttemptCredentials.email)
            if not user:
                return False

            success = user.compareCredentials(loginAttemptCredentials)
            return success

    def ifUserExists(self, email: EmailModel) -> bool:
        with self.db.begin() as session:
            result = session.execute(
                select(SqliteEmailModel).where(SqliteEmailModel.value == email.value)
            ).fetchone()
            if not result:
                return False
            return True
