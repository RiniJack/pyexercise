import config
import logging
import time

logger = logging.getLogger(__name__)


class UsersDB:

    def __init__(self, application):
        self.application = application

    def get_users(self):
        db = self.application.database
        try:
            return db[config.USERS_DB].find()
        except Exception as e:
            logging.exception("Failed to get users from DB")
            raise

    def find_user(self, user_name):
        db = self.application.database
        try:
            return db[config.USERS_DB].find({config.USER_NAME: user_name});
        except Exception as e:
            logging.exception("Failed to find user in DB")
            raise

    def create_user(self, user):
        db = self.application.database
        try:
            user[config.CREATION_TIME] = time.time()
            db.users.insert(user)
        except Exception as e:
            logging.exception("Failed to create user in DB")
            raise


class PostsDB:

    def __init__(self, application):
        self.application = application

    def get_posts(self, user_name, limit):
        db = self.application.database
        try:
            return db[config.POSTS_DB].find({config.USER_NAME: user_name})\
                .limit(int(limit))#.sort({config.CREATION_TIME: 1})
        except Exception as e:
            logging.exception("Failed to get posts from DB")
            raise

    def create_post(self, post):
        db = self.application.database
        try:
            post[config.CREATION_TIME] = time.time()
            db.posts.insert(post)
            # db.posts.update({post},{ "$currentDate": { "date": { "$type": "date" }}})
        except Exception as e:
            logging.exception("Failed to create post in DB")
            raise