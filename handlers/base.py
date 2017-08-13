import config
import logging
import json

from tornado.web import RequestHandler, HTTPError
from database.db import UsersDB, PostsDB
from bson.json_util import dumps
from multiprocessing.pool import ThreadPool
from tornado.ioloop import IOLoop
from tornado.web import asynchronous

logger = logging.getLogger(__name__)
_workers = ThreadPool(10)


class BaseHandler(RequestHandler):
    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        RequestHandler.__init__(self, application, request, **kwargs)

        self.userDb = UsersDB(self.application)
        self.postDb = PostsDB(self.application)

        self.set_header("Content-Type", "application/json")

    @asynchronous
    def get_async(self, func, callback):
        self.run_in_background(func, callback)

    @asynchronous
    def get_async(self, func, callback, args=(), kwds={}):
        def _callback(result):
            IOLoop.instance().add_callback(lambda: callback(result))
        _workers.apply_async(func, args, kwds, _callback)

    def parse_request_body(self, body):
        if not body:
            raise HTTPError(400, "Missing request body")
        try:
            data = json.loads(self.request.body)
            if not data:
                raise HTTPError(400, "Missing request body")
            return data
        except ValueError:
            raise HTTPError(400, "Unable to parse request body")

    def write_successful_response(self, message=None, data=None):
        logger.debug("Writing successful response [message:%s]", message)
        self.finish(dumps({
            config.CODE: 200,
            config.MESSAGE: message,
            config.DATA: data
        }))

    def write_failed_response(self, message=None, error=None, status_code=500):
        logger.debug("Writing failed response [message:%s, error:%s, code:%s]", message, error, status_code)
        self.set_status(status_code)
        self.finish(dumps({
            config.CODE: status_code,
            config.MESSAGE: message,
            config.ERROR: error
        }))

