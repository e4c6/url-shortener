import os
from sqlalchemy.orm import sessionmaker
from src.Adapters.IDbAdapter import IDbAdapter
from src.Adapters.SqliteAdapter import SqliteAdapter
from src.IConfig import IConfig
from src.Services.IUrlShortenerService import IUrlShortenerService
from src.Services.IUserService import IUserService
from src.Services.UrlShortenerService import UrlShortenerService
from src.Services.UserService import UserService


class SqliteConfig(IConfig):
    jwtSecret = None
    dbClient: sessionmaker = None
    userService: IUserService = None
    urlShortenerService: IUrlShortenerService = None
    dbAdapter: IDbAdapter = None
    passwordSalt: str = None
    minimumShortUrlLength: int = 4

    @staticmethod
    def initConfig() -> None:
        from src import SqliteDb
        from src.Models.ORM.SqlAlchemy.SqliteUrlModel import SqliteUrlModel
        from src.Models.ORM.SqlAlchemy.SqliteUrlKeyModel import SqliteUrlKeyModel
        from src.Models.ORM.SqlAlchemy.SqliteUserModel import SqliteUserModel
        from src.Models.ORM.SqlAlchemy.SqlitePasswordHashModel import SqlitePasswordHashModel
        from src.Models.ORM.SqlAlchemy.SqliteEmailModel import SqliteEmailModel

        SqlitePasswordHashModel.metadata.create_all(SqliteDb.engine)
        SqliteUserModel.metadata.create_all(SqliteDb.engine)
        SqliteUrlModel.metadata.create_all(SqliteDb.engine)
        SqliteUrlKeyModel.metadata.create_all(SqliteDb.engine)
        SqliteEmailModel.metadata.create_all(SqliteDb.engine)

        from dotenv import load_dotenv
        load_dotenv()

        SqliteConfig.jwtSecret = os.getenv('JWT_SECRET')
        SqliteConfig.passwordSalt = os.getenv('PASSWORD_HASH_SALT')
        SqliteConfig.dbClient = SqliteDb.SessionLocal
        SqliteConfig.dbAdapter = SqliteAdapter(SqliteConfig.dbClient, SqliteConfig.passwordSalt)
        SqliteConfig.userService = UserService(SqliteConfig.dbAdapter, SqliteConfig.jwtSecret)
        SqliteConfig.urlShortenerService = UrlShortenerService(SqliteConfig.dbAdapter,
                                                               SqliteConfig.minimumShortUrlLength)





