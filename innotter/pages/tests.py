from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from pages.models import Page


class PagesTests(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(username='root', email='root@gmail.com', password='rootroot')
        self.testuser = User.objects.create_user(username='testtest', email='testtest@gmail.com', password='testtest')
        self.user = User.objects.create_user(username='useruser', email='useruser@gmail.com', password='useruser')
        self.testuuid = 123
        Page.objects.create_page(name='testpage',owner=self.user,uuid=self.testuuid, tags="")
        # self.client.login(username='root', password='rootroot')
        # self.client.force_authenticate(self.superuser)
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
        self.client.force_authenticate(self.testuser)
        response = self.client.post(url,self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_all_pages_admin(self):
        url = '/pages/list_all_users/'
        self.client.force_authenticate(self.superuser)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_all_pages_not_admin(self):
        url = '/pages/list_all_users/'
        self.client.force_authenticate(self.testuser)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_my_page(self):
        url = '/pages/my_pages/'
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_page(self):
        url = f'/pages/{self.testuuid}/update_page/'
        self.client.force_authenticate(self.user)
        data = {
            "name": "anonimous",
            "uuid": self.testuuid,
            "is_private": "0",
            "description": "sus",
            "image": "https://i.insider.com/601c27acee136f00183aa4f5",
            "tags": ["tag2"]
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(Page.objects.get(uuid=self.testuuid).name)
        self.assertEqual(Page.objects.get(uuid=self.testuuid).name, data["name"])
        self.assertEqual(Page.objects.get(uuid=self.testuuid).description, data["description"])
        self.assertEqual(Page.objects.get(uuid=self.testuuid).image, data["image"])
