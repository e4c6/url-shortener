from flask_restful import Resource
from flask import request
from src.Controllers.Helpers.ExceptionHandler import ExceptionHandler
from src.Controllers.Helpers.TokenRequired import TokenRequired
from src.Models.UrlKeyModel import UrlKeyModel
from src.Models.UrlModel import UrlModel
from src.Services.IUrlShortenerService import IUrlShortenerService
from src.config import Config

class ShortUrlController(Resource):
    def __init__(self):
        self.urlShortenerService: IUrlShortenerService = Config.urlShortenerService

    @ExceptionHandler
    @TokenRequired
    def put(self):
        longUrl: UrlModel = UrlModel(request.form['longUrl'])
        shortUrl: UrlKeyModel = self.urlShortenerService.createShortUrl(longUrl)

        return {'shortUrl': shortUrl.toPath()}
