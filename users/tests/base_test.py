from django.test import TestCase
from users.models import User
from faker import Faker


class NewUserTestCase(TestCase):

    def setUp(self) -> None:
        faker = Faker()
        self.email = faker.email()
        self.username = faker.user_name()
        self.password = faker.password()
        self.firstname = faker.first_name()
        self.user = User.objects.create_user(
            email=self.email,
            username=self.username,
            password=self.password,
            first_name=self.firstname
        )

    def tearDown(self) -> None:
        self.user.delete()
