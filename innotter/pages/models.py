from django.db import models
from django.contrib.auth.models import BaseUserManager
from datetime import datetime


class PageManager(BaseUserManager):
    def create_page(self, name, owner, uuid, tags, description='', image='', is_private=False):
        if name is None:
            raise TypeError('Pages must have a name.')
        if uuid is None:
            raise TypeError('Pages must have uuid')

        page = self.model(
            name=name,
            owner=owner,
            uuid=uuid,
            description=description,
            image=image,
            is_private=is_private,
            # tags=tags,

        )

        page.unblock_date = datetime.now()
        page.save()
        page.tags.set(tags)
        page.save()

        return page

    def update_page(self, page, name, description='', image='', is_private=False):
        if name is None:
            raise TypeError('Pages must have a name.')
        page.name = name
        page.description = description
        page.image = image
        page.is_private = is_private
        page.save()
        return page

    def delete_page(self, page):
        page.unblock_date = datetime.max
        page.save()
        return page

    def block_page(self, page, unblock_date):
        page.unblock_date = unblock_date
        page.save()
        return page

    def add_follower(self, page, follower):
        page.followers.add(follower)
        return page

    def add_follow_request(self, page, follower):
        page.follow_requests.add(follower)
        return page

    def apply_all_follow_requests(self, page):
        page.followers += page.follow_requests
        return page


class Page(models.Model):
    name = models.CharField(max_length=64)
    uuid = models.CharField(max_length=64,primary_key=True, unique=True)
    description = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField('tags.Tag', related_name='pages')

    owner = models.ForeignKey(

        'users.User', on_delete=models.CASCADE, related_name='user_id'
    )

    followers = models.ManyToManyField('users.User', related_name='follows')

    image = models.URLField(null=True, blank=True)

    is_private = models.BooleanField(default=False)

    follow_requests = models.ManyToManyField('users.User',
                                             related_name='requests')

    unblock_date = models.DateTimeField(null=True, blank=True)

    objects = PageManager()
