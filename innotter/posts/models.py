from datetime import datetime

from django.core.mail import send_mail
from django.db import models
from django.http import HttpResponse

from innotter.celery import post_created_task
from pages.models import Page
from users.models import User
from posts.tasks import post_created


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

        #уведомление о новой записи по емаилу
        post_created_task(content, page, reply_to)

        return post

    # def send_mail(self, content, page, reply_to):
    #     recipient_list = page.followers.values('email')
    #     recipient_list = [email['email'] for email in recipient_list]
    #     res = send_mail(
    #         subject=f'{page.name} posted new post! Check it!',
    #         message=content,
    #         from_email='innotter@gmail.com',
    #         recipient_list = recipient_list,
    #         fail_silently=False,
    #     )
    #
    #     return print(f"Email sent to {res} members")


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
