from datetime import datetime
from django.db import models
from innotter.celery import post_created_task
from pages.models import Page
from users.models import User


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

        # notification
        # post_created_task.apply_async(content, page.uuid, reply_to.id)
        post_created_task.apply_async(args=[content, page.uuid, reply_to.id])
        return post

    def update_post(self, post, content):
        post.content = content
        post.updated_at = datetime.now()
        post.save()
        return post

    def add_like(self, post, liker):
        post.liked_by.add(liker)
        post.save()
        return post

    def remove_like(self, post, liker):
        post.liked_by.remove(liker)
        return post


class Post(models.Model):
    content = models.CharField(max_length=256)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='post_to_page')

    reply_to = models.ForeignKey(
        'users.User', on_delete=models.SET_NULL, null=True
    )

    liked_by = models.ManyToManyField(User, null=True, related_name='users_liked')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PostManager()
