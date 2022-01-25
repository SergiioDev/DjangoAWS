from rest_framework.test import APIClient
from organizations.models import Organization
from users.tests import base_test


class OrganizationTestCreateCase(base_test.NewUserTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        self.login_response = self.client.post('/api/v1/users/token',
                                               {'email': self.email,
                                                'username': self.username,
                                                'password': self.password, })

        self.access_token = self.login_response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_organization_create(self):
        self.create_organization_response = self.client.post('/api/v1/organizations/',
                                                             {'name': 'Organization name',
                                                              'registration_code': '5555',
                                                              'established_on': '2001-10-03'})
        self.assertEquals(self.create_organization_response.status_code, 201)
        self.assertEquals('Success', self.create_organization_response.json()['status'])
        self.assertEquals('Organization created!', self.create_organization_response.json()['message'])
        self.assertEquals('Organization name', self.create_organization_response.json()['Organization']['name'])
        self.assertEquals('5555', self.create_organization_response.json()['Organization']['registration_code'])
        self.assertEquals('2001-10-03', self.create_organization_response.json()['Organization']['established_on'])

    def tearDown(self) -> None:
        self.client.logout()
        Organization.objects.filter().delete()
        super().tearDown()


class OrganizationListCase(base_test.NewUserTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.client = APIClient()
        self.login_response = self.client.post('/api/v1/users/token',
                                               {'email': self.email,
                                                'username': self.username,
                                                'password': self.password, })

        self.access_token = self.login_response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        self.organization = Organization.objects.create(name='Organization name', registration_code='5555',
                                                        established_on='2001-10-03')

    def test_organization_list(self):
        self.list_response = self.client.get('/api/v1/organizations/')
        self.assertEquals('Success', self.list_response.json()['status'])
        self.assertTrue('Organization name', self.list_response.json()['Organizations'][0]['name'])

    def tearDown(self) -> None:
        self.client.logout()
        Organization.objects.filter().delete()
        super().tearDown()


class OrganizationByIdCase(base_test.NewUserTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.client = APIClient()
        self.login_response = self.client.post('/api/v1/users/token',
                                               {'email': self.email,
                                                'username': self.username,
                                                'password': self.password, })

        self.access_token = self.login_response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        self.organization = Organization.objects.create(name='Organization one', registration_code='5555',
                                                        established_on='2001-10-03')

    def test_organization_by_id(self):
        self.organization_by_id_response = self.client.get('/api/v1/organizations/2/')
        self.assertEquals(self.organization_by_id_response.status_code, 200)

        self.assertEquals('Success', self.organization_by_id_response.json()['status'])
        self.assertEquals('Organization found', self.organization_by_id_response.json()['message'])
        self.assertEquals('Organization one', self.organization_by_id_response.json()['Organization']['name'])
        self.assertEquals('5555', self.organization_by_id_response.json()['Organization']['registration_code'])
        self.assertEquals('2001-10-03', self.organization_by_id_response.json()['Organization']['established_on'])

    def tearDown(self) -> None:
        self.client.logout()
        Organization.objects.filter().delete()
        super().tearDown()


class DeleteOrganizationByIdCase(base_test.NewUserTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.client = APIClient()
        self.login_response = self.client.post('/api/v1/users/token',
                                               {'email': self.email,
                                                'username': self.username,
                                                'password': self.password, })

        self.access_token = self.login_response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        self.organization = Organization.objects.create(name='Organization name', registration_code='6555',
                                                        established_on='2001-10-03')

    def test_delete_organization_by_id(self):
        self.delete_organization_by_id_response = self.client.delete('/api/v1/organizations/1/')
        self.assertEquals(self.delete_organization_by_id_response.status_code, 202)

        self.assertEquals('Success', self.delete_organization_by_id_response.json()['status'])
        self.assertEquals('Organization deleted', self.delete_organization_by_id_response.json()['message'])

    def tearDown(self) -> None:
        self.client.logout()
        Organization.objects.filter().delete()
        super().tearDown()
