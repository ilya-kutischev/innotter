from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User


class PagesTests(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(username='root', email='root@gmail.com', password='rootroot')
        self.user = User.objects.create_user(username='testtest', email='testtest@gmail.com', password='testtest')
        self.client.login(username='root', password='rootroot')
        self.client.force_authenticate(self.superuser)
        self.data = {
    "name": "s23uws",
    "uuid": 122,
    "is_private": "0",
    "description": "sus",
    "image": "https://i.insider.com/601c27acee136f00183aa4f5",
    "tags": ["tag1", "tag2"]
}

    def test_create_page(self):
        url = '/pages/create_page/'
        response = self.client.post(url,self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

