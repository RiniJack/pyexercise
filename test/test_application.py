import tornado
from tornado.web import Application
from urls import urls
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from test import config_test


class Application(Application):
    def __init__(self):
        handlers = urls

        settings = dict(
            autoescape=None,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        try:
            self.con = MongoClient(config_test.DB_CONN_STR)
            self.database = self.con[config_test.DB_NAME]
        except Exception as e:
            raise ConnectionFailure("Failed to connect to db", e)