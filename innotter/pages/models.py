from django.db import models
from django.contrib.auth.models import BaseUserManager


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)


class PageManager(BaseUserManager):
    def create_page(self, name,owner, uuid, description='', image='', is_private=False):
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
        )
        page.save()

        return page


class Page(models.Model):
    name = models.CharField(max_length=64)
    uuid = models.CharField(max_length=64, unique=True)
    description = models.TextField(null=True, blank=True)
    # tags = models.ManyToManyField('users.Tag', related_name='pages')

    owner = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='user_id'
    )
    followers = models.ManyToManyField(
        'users.User', related_name='follows', null=True, blank=True
    )

    image = models.URLField(null=True, blank=True)

    is_private = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField(
        'users.User', related_name='requests', null=True, blank=True
    )

    unblock_date = models.DateTimeField(null=True, blank=True)

    objects = PageManager()


class Post(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='posts')
    content = models.CharField(max_length=256)

    reply_to = models.ForeignKey(
        'users.User', on_delete=models.SET_NULL, null=True, related_name='replies'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
