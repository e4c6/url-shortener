import os
from google.cloud.firestore_v1 import Client
from src.Adapters.FirestoreAdapter import FirebaseAdapter
from src.Adapters.IDbAdapter import IDbAdapter
from src.IConfig import IConfig
from src.Services.IUrlShortenerService import IUrlShortenerService
from src.Services.IUserService import IUserService
from src.Services.UrlShortenerService import UrlShortenerService
from src.Services.UserService import UserService
from google.cloud import firestore

class FirestoreConfig(IConfig):
    jwtSecret = None
    dbClient: Client = None
    userService: IUserService = None
    urlShortenerService: IUrlShortenerService = None
    dbAdapter: IDbAdapter = None
    passwordSalt: str = None
    minimumShortUrlLength: int = 4

    @staticmethod
    def initConfig() -> None:
        from dotenv import load_dotenv
        load_dotenv()

        FirestoreConfig.jwtSecret = os.getenv('JWT_SECRET')
        FirestoreConfig.passwordSalt = os.getenv('PASSWORD_HASH_SALT')
        FirestoreConfig.dbClient = firestore.Client.from_service_account_info({
            "project_id": os.getenv('project_id'),
            "private_key": os.getenv('private_key'),
            "client_email": os.getenv('client_email'),
            "token_uri": os.getenv('token_uri'),
        })

        FirestoreConfig.dbAdapter = FirebaseAdapter(FirestoreConfig.dbClient, FirestoreConfig.passwordSalt)
        FirestoreConfig.userService = UserService(FirestoreConfig.dbAdapter, FirestoreConfig.jwtSecret)
        FirestoreConfig.urlShortenerService = UrlShortenerService(FirestoreConfig.dbAdapter, FirestoreConfig.minimumShortUrlLength)
