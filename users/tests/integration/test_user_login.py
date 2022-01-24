from rest_framework.test import APIClient
from users.tests import base_test


class UserLoginTestCase(base_test.NewUserTestCase):

    def setUp(self) -> None:
        super().setUp()

    def test_user_login(self):
        client = APIClient()
        result = client.post('/api/v1/users/token', {'email': self.email,
                                                     'username': self.username,
                                                     'password': self.password}, format='json')

        self.assertEquals(result.status_code, 200)
        self.assertTrue('access' in result.json())
        self.assertTrue('refresh' in result.json())

    def tearDown(self) -> None:
        self.client.logout()
        super().tearDown()


class RefreshAccessTokenTestCase(base_test.NewUserTestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_user_login(self):
        client = APIClient()
        acess_token = client.post('/api/v1/users/token', {'email': self.email,
                                                          'username': self.username,
                                                          'password': self.password}, format='json')

        refresh_access_token = client.post('/api/v1/users/token', {'email': self.email,
                                                                   'password': self.password,
                                                                   'refresh': acess_token.json()['refresh']},
                                           format='json')

        self.assertTrue(acess_token.json()['access'] != refresh_access_token.json()['access'])
