from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User


class AccountTests(APITestCase):
    def setUp(self):
        User.objects.create_superuser(username='root', email='root@gmail.com', password='rootroot')

    def test_create_account(self):
        url = '/register/'
        data = {
            "username": "testtest",
            "password": "testtest",
            "email": "testtest@gmail.com",
            "role": "user",
            "title": "test"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 2)

    def test_login(self):
        url = '/login/'
        data = {
            "email": "root@gmail.com",
            "password": "rootroot"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_accounts(self):
        url = '/list_all_users/'
        self.client.force_login(User.objects.get(username="root"))
        response = self.client.get(url)
        print(response.data)
        self.assertTrue(response.data is not None)
