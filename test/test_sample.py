import os.path, sys
import json
from tornado.testing import AsyncHTTPTestCase
import test_application

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(APP_ROOT, '..'))

# tornado.options.parse_config_file(os.path.join(APP_ROOT, 'test/config', 'config_test.py'))
app = test_application.Application()


def clear_db(app=None):
    app.database.drop_collection("users")


class TestHandlerBase(AsyncHTTPTestCase):
    def setUp(self):
        super(TestHandlerBase, self).setUp()

    @classmethod
    def setUpClass(cls):
        clear_db(app)
        super(TestHandlerBase, cls).setUpClass()

    def get_app(self):
        return app

    # def get_http_port(self):
    #     return options.port


class TestUsersHandler(TestHandlerBase):
    def test_get_users(self):
        response = self.fetch(
            '/users/get',
            method='GET')
        response_data = self.validate_response(response, 200);
        self.assertEqual(response_data['message'], 'Get users completed successfully')
        self.assertEqual(len(response_data['data']), 1)
        user = response_data['data'][0]
        self.assertEqual(user['userName'], 'e2etest')
        self.assertEqual(user['firstName'], 'e2e')
        self.assertEqual(user['lastName'], 'test')
        self.assertEqual(user['email'], 'e2etest@gmail.com')
        self.assertEqual(user['phone'], '050-12345678')

    def test_create_user(self):
        data = '{' \
               '"userName": "e2etest",' \
               '"firstName": "e2e", ' \
               '"lastName": "test", ' \
               '"email": "e2etest@gmail.com", "' \
               'phone": "050-12345678"}'

        response = self.fetch('/users/create',
                              method="POST",
                              body=data)
        response_data = self.validate_response(response, 200);
        self.assertEqual(response_data['message'], "User 'e2etest' created successfully")

        response = self.fetch('/users/create',
                              method="POST",
                              body=data)
        response_data = self.validate_response(response, 500);
        self.assertEqual(response_data['message'], "Failed to create user")
        self.assertEqual(response_data['error'], "User name 'e2etest' already exists")

    def validate_response(self, response, code):
        self.assertEqual(response.code, code)
        self.assertIsNotNone(response.body)
        response_data = json.loads(response.body)
        self.assertIsNotNone(response_data)
        return response_data
