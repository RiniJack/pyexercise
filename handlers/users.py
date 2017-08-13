import config
import logging
import time

from base import BaseHandler
from tornado.web import HTTPError
from tornado.web import asynchronous

logger = logging.getLogger(__name__)


class GetUsersHandler(BaseHandler):

    @asynchronous
    def get(self):
        self.get_async(self.get_users, self.on_complete)

    def on_complete(self, response):
        self.finish()

    def get_users(self):
        try:
            users = self.userDb.get_users()
            logger.debug("Found %s users in DB", users.count())
            self.write_successful_response("Get users completed successfully", users)
        except Exception as e:
            logging.exception("Failed to get users")
            self.write_failed_response("Failed to get users", e.message)


class CreateUserHandler(BaseHandler):

    def post(self):
        try:
            data = self.parse_request_body(self.request.body)
            user_name = self.validate_user(data)
            self.userDb.create_user(data)
            message = "User '{}' created successfully".format(user_name)
            logging.info(message)
            self.write_successful_response(message)
        except HTTPError as err:
            logging.exception("HTTPError in create user")
            self.write_failed_response("Failed to create user", err.log_message, err.status_code)
        except Exception as e:
            logging.exception("Error in create user")
            self.write_failed_response("Failed to create user", e.message)

    def validate_user(self, data):
        if config.USER_NAME not in data:
            raise HTTPError(400, "User name is missing")

        user_name = data[config.USER_NAME]
        user = self.userDb.find_user(user_name)
        if user.count() > 0:
            raise Exception("User name '{}' already exists".format(user_name))
        return user_name