# Para crear datos fake
from faker import Faker

from rest_framework import status
from rest_framework.test import APITestCase

class TestSetUp(APITestCase):
    
    def setUp(self):
        from apps.users.models import User

        faker = Faker()

        self.login_url = '/login/'
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
                'password': 'developer'
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #import pdb; pdb.set_trace()

        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        return super().setUp()
    
    def test_prueba(self):
        pass