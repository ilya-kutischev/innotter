from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from datetime import datetime, timedelta
from django.conf import settings
import jwt


class UserManager(BaseUserManager):
    """
    Django требует, чтобы кастомные пользователи определяли свой собственный
    класс Manager. Унаследовавшись от BaseUserManager, мы получаем много того
    же самого кода, который Django использовал для создания User (для демонстрации).
    """

    def create_user(self, username, email, password=None):
        """Создает и возвращает пользователя с имэйлом, паролем и именем."""
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def update_user(self, user, username, email, password=None):
        """Изменяет и возвращает пользователя с имэйлом, паролем и именем."""
        if username is None:
            raise TypeError('Enter username.')

        if email is None:
            raise TypeError('Enter an email address.')
        user.username = username
        user.email = email
        user.password = password
        # user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """Создает и возввращет пользователя с привилегиями суперадмина."""
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

    title = models.CharField(max_length=80)
    is_blocked = models.BooleanField(default=False)

    objects = UserManager()

    @property
    def token(self):
        """
        Позволяет получить токен пользователя путем вызова user.token, вместо
        user._generate_jwt_token(). Декоратор @property выше делает это
        возможным. token называется "динамическим свойством".
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Генерирует веб-токен JSON, в котором хранится идентификатор этого
        пользователя, срок действия токена составляет 1 день от создания
        """
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode(
            {'id': self.pk, 'exp': int(dt.strftime('%s'))},
            settings.SECRET_KEY,
            algorithm='HS256',
        )

        return token.decode('utf-8')


# INTERFACE INNOTTER REALISATION
class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Page(models.Model):
    name = models.CharField(max_length=64)
    uuid = models.CharField(max_length=64, unique=True)
    description = models.TextField()
    tags = models.ManyToManyField('users.Tag', related_name='pages')

    owner = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='pages'
    )
    followers = models.ManyToManyField('users.User', related_name='follows')

    image = models.URLField(null=True, blank=True)

    is_private = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField('users.User', related_name='requests')

    unblock_date = models.DateTimeField(null=True, blank=True)


class Post(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='posts')
    content = models.CharField(max_length=256)

    reply_to = models.ForeignKey(
        'users.Post', on_delete=models.SET_NULL, null=True, related_name='replies'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
