from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.is_blocked = False
        user.IsActive = True
        user.save()

        return user

    def update_user(self, user, username, email, password=None):
        if username is None:
            raise TypeError('Enter username.')

        if email is None:
            raise TypeError('Enter an email address.')
        user.username = username
        user.email = email
        user.password = password
        user.set_password(password)
        user.save()

        return user

    def delete_user(self, user):
        user.is_active = False
        user.save()
        return user


    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    email = models.EmailField(unique=True)
    image_s3_path = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=9, choices=Roles.choices)
    is_active = models.BooleanField(default=True)
    title = models.CharField(max_length=80)
    is_blocked = models.BooleanField(default=False)

    objects = UserManager()
