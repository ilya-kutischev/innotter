from datetime import datetime
from django.db import models
from pages.models import Page


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)


class PostManager(models.Manager):
    def create_post(self, content, page, reply_to):
        if page is None:
            raise TypeError('Pages must have related page')

        post = self.model(
            content=content,
            page=page,
            reply_to=reply_to,
        )
        post.save()

        return post

    def update_post(self, post, content):
        post.content = content
        post.updated_at = datetime.now()
        post.save()
        return post


class Post(models.Model):
    content = models.CharField(max_length=256)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='pages_id')

    reply_to = models.ForeignKey(
        'users.User', on_delete=models.SET_NULL, null=True, related_name='replies'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PostManager()
