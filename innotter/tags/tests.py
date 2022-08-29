from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from pages.models import Page
from tags.models import Tag
from users.models import User


class TagsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', email='user@gmail.com', password='useruser')
        self.testuuid = 123
        self.data = {
            "name": "s23uws",
            "uuid": 122,
            "is_private": "0",
            "description": "sus",
            "image": "https://i.insider.com/601c27acee136f00183aa4f5",
            "tags": ["tag1", "tag2"]
        }

    def test_create_tag(self):
        url = '/pages/create_page/'
        self.assertEqual(Tag.objects.count(), 0)
        self.client.force_authenticate(self.user)
        self.client.post(url, self.data)
        self.assertEqual(Tag.objects.count(), len(self.data["tags"]))
