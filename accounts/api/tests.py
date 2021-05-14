from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User


LOGIN_URL = '/api/accounts/login/'
LOGOUT_URL = '/api/accounts/logout/'
SIGNUP_URL = '/api/accounts/signup/'
LOGIN_STATUS_URL = '/api/accounts/login_status/'


class AccountApiTests(TestCase):

    def setUp(self):
        # this function will be executed in each test function
        self.client = APIClient()
        self.user = self.createUser(
            username='admin',
            email='admin@twitter.com',
            password='correct password',
        )

    def createUser(self, username, email, password):
        return User.objects.create_user(username, email, password)

    def test_login(self):
        response = self.client.get(LOGIN_URL, {
            'username': self.user.username,
            'password': 'correct password',
        })

        # if login failed, return response with status code = 405
        self.assertEqual(response.status_code, 405)

        # return 400 when password is incorrect
        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'wrong password',
        })
        self.assertEqual(response.status_code, 400)

        # assert that login status is false before successfully login
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)
        # when providing correct password
        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'correct password'
        })
        # return 200
        self.assertEqual(response.status_code, 200)
        # return user data is not empty
        self.assertNotEqual(response.data['user'], None)
        # assert email
        self.assertEqual(response.data['user']['email'], 'admin@twitter.com')
        # assert login status
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)

    def test_logout(self):
        self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'correct password'
        })
        # assert user successfully logged in
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)

        # return 405 when call with GET method
        response = self.client.get(LOGOUT_URL)
        self.assertEqual(response.status_code, 405)

        # return 200 when successfully logout
        response = self.client.post(LOGOUT_URL)
        self.assertEqual(response.status_code, 200)
        # assert login status
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)

    def test_signup(self):
        data = {
            'username': 'someone',
            'email': 'someone@twitter.com',
            'password': 'correct password',
        }

        # return 405 when call with GET method
        response = self.client.get(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 405)

        # return 400 when email format is incorrect
        response = self.client.post(SIGNUP_URL,{
            'username': 'someone',
            'email': 'incorrect format',
            'password': 'correct password',
        })
        self.assertEqual(response.status_code, 400)

        # return 400 when password is too short
        response = self.client.post(SIGNUP_URL,{
            'username': 'someone',
            'email': 'soemone@some.com',
            'password': '123',
        })
        self.assertEqual(response.status_code, 400)

        # return 400 when username is too long
        response = self.client.post(SIGNUP_URL, {
            'username': 'a very long user name that will exceed the max allowed length',
            'email': 'someone@some.com',
            'password': '123456'
        })
        self.assertEqual(response.status_code, 400)

        # successfully signup
        response = self.client.post(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user']['username'], 'someone')
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)