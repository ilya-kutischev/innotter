from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User


class AccountTests(APITestCase):
    def setUp(self):
        User.objects.create_superuser(username='root', email='root@gmail.com', password='rootroot')
        User.objects.create_user(username='user', email='user@gmail.com', password='useruser')

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
        self.assertEqual(User.objects.count(), 3)

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

    def test_delete_account(self):
        url = '/delete_user/'
        self.client.force_login(User.objects.get(username="user"))
        self.client.force_authenticate(User.objects.get(username="user"))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(username="user").is_active, False)

    def test_update_account(self):
        url = '/update_user/'
        self.client.force_login(User.objects.get(username="user"))
        self.client.force_authenticate(User.objects.get(username="user"))
        data = {
            "username": "testtest",
            "password": "testtest",
            "email": "testtest@gmail.com",
            "role": "user",
            "title": "test"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


