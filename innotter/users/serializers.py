from rest_framework import serializers
from users.models import User


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# class RegistrationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['email', 'username', 'password', 'password_confirmation']
#         extra_kwargs = {'password' = {'write_only': True}
#         }
