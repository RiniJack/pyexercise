from handlers.users import GetUsersHandler, CreateUserHandler
from handlers.posts import GetPostsHandler, CreatePostHandler

urls = [
    [r'/users/get', GetUsersHandler],
    [r'/users/create', CreateUserHandler],
    [r'/posts/get', GetPostsHandler],
    [r'/posts/create', CreatePostHandler],
]