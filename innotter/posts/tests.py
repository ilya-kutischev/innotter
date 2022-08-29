from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from pages.models import Page


class PostsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='useruser', email='useruser@gmail.com', password='useruser')
        self.testuuid = 123
        Page.objects.create_page(name='testpage',owner=self.user,uuid=self.testuuid, tags="")

    def test_create_post(self):
        url = f'/pages/page/{self.testuuid}/posts/create_post/'
        self.client.force_authenticate(self.user)
        data = {
            "content": "content",
            "reply_to": ""
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
