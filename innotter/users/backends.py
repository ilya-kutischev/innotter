from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class UserBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        user_email = kwargs['email']
        password = kwargs['password']
        try:
            user = User.objects.get(email=user_email)
            if user.check_password(password) is True:
                return user
        except User.DoesNotExist:
            pass
