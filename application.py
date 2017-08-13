import tornado
import config
import logging

from tornado.web import Application
from tornado.options import define, options, parse_command_line
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from urls import urls
from logging.config import fileConfig

define("port", default=12345, help="run on the given port", type=int)
logger = logging.getLogger(__name__)


class Application(Application):
    def __init__(self):
        handlers = urls

        settings = dict(
            autoescape=None,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        try:
            self.con = MongoClient(config.DB_CONN_STR)
            self.database = self.con[config.DB_NAME]
        except Exception as e:
            raise ConnectionFailure("Failed to connect to db", e)


def main():
    logging.basicConfig(filename='logs/server.log', filemode='w', level=logging.INFO)
    #fileConfig('log.ini')
    parse_command_line()
    http_server = HTTPServer(Application())
    http_server.listen(options.port)
    logger.info('Server is running at http://localhost:%s', options.port)
    IOLoop.instance().start()


if __name__ == "__main__":
    main()