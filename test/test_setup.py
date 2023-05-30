# Para crear datos fake
from faker import Faker

from rest_framework.test import APITestCase

class TestSetUp(APITestCase):
    
    def setup(self):
        from apps.users.models import User

        faker = Faker()

        self.login_url = '/login'
        self.user = User.objects.create_superuser(
            name='Developer',
            last_name='Backend',
            username='developer',
            password='developer',
            email= faker.email()
        )

        response = self.client.post(
            self.login_url,
            {
                'username': self.user.username,
                'password': self.user.password
            },
            format='json'
        )

        self.token = response.data['token']