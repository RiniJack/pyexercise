import config
import logging

from base import BaseHandler
from tornado.web import HTTPError

logger = logging.getLogger(__name__)


class GetPostsHandler(BaseHandler):
    def get(self):
        try:
            user_name = self.get_argument('userName', None)
            if not user_name:
                raise HTTPError(400, "'userName' parameter is missing")
            limit = self.get_argument('limit', None)
            if not limit:
                raise HTTPError(400, "'limit' parameter is missing. You must limit the number of requested posts")

            posts = self.postDb.get_posts(user_name,limit)
            logger.debug("Found %s posts for user %s in DB", posts.count(), user_name)
            self.write_successful_response("Get posts completed successfully", posts)
        except Exception as e:
            logging.exception("Failed to get posts")
            self.write_failed_response("Failed to get posts", e.message)


class CreatePostHandler(BaseHandler):

    def post(self):
        try:
            data = self.parse_request_body(self.request.body)
            user_name = self.validate_post_data(data)
            self.postDb.create_post(data)
            message = "New post created successfully on {}'s wall".format(user_name)
            logging.info(message)
            self.write_successful_response(message)
        except HTTPError as err:
            logging.exception("HTTPError in create post")
            self.write_failed_response("Failed to create post", err.log_message, err.status_code)
        except Exception as e:
            logging.exception("Error in create post")
            self.write_failed_response("Failed to create post", e.message)

    def validate_post_data(self, data):
        if config.USER_NAME not in data:
            raise HTTPError(400, "User name is missing")
        if config.CREATED_BY not in data:
            raise HTTPError(400, "Created by is missing")
        if config.DATA not in data:
            raise HTTPError(400, "This post has no data")

        user_name = data[config.USER_NAME]
        user = self.userDb.find_user(user_name)
        if user.count() == 0:
            raise Exception("User name '{}' dose not exists".format(user_name))
        return user_name