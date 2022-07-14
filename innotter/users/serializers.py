from rest_framework import serializers
from users.models import User
from datetime import datetime, timedelta
import jwt
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from innotter.settings import JWT_SECRET, JWT_ACCESS_TTL, JWT_REFRESH_TTL


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    # token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'image_s3_path', 'role', 'title')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'image_s3_path', 'role', 'title')
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, validated_data):
        return User.objects.update_user(**validated_data)


class DeleteSerializer(serializers.ModelSerializer):
    def delete(self, validated_data):
        return User.objects.delete_user(**validated_data)


# Authentification!

UserModel = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ('__all__')
        fields = ('email', 'password', 'refresh', 'access')

    # ==== INPUT ====
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    # ==== OUTPUT ====
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        # standard validation
        validated_data = super().validate(attrs)

        # validate email and password
        email = validated_data['email']
        password = validated_data['password']
        error_msg = _('email or password are incorrect')
        try:
            user = UserModel.objects.get(email=email)
            if not user.check_password(password):
                raise serializers.ValidationError(error_msg)
            validated_data['user'] = user
        except UserModel.DoesNotExist:
            raise serializers.ValidationError(error_msg)

        return validated_data

    def create(self, validated_data):
        access_payload = {
            'iss': 'backend-api',
            'user_id': validated_data['user'].id,
            'exp': datetime.utcnow() + timedelta(seconds=JWT_ACCESS_TTL),
            'type': 'access',
        }
        access = jwt.encode(payload=access_payload, key=JWT_SECRET)

        refresh_payload = {
            'iss': 'backend-api',
            'user_id': validated_data['user'].id,
            'exp': datetime.utcnow() + timedelta(seconds=JWT_REFRESH_TTL),
            'type': 'refresh',
        }
        refresh = jwt.encode(payload=refresh_payload, key=JWT_SECRET)

        return {'access': access, 'refresh': refresh}


class RefreshSerializer(serializers.Serializer):
    # ==== INPUT ====
    refresh_token = serializers.CharField(required=True, write_only=True)
    # ==== OUTPUT ====
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = 'refresh_token'

    def validate(self, attrs):
        # standard validation
        validated_data = super().validate(attrs)

        # validate refresh
        refresh_token = validated_data['refresh_token']
        try:
            payload = jwt.decode(refresh_token, JWT_SECRET)
            if payload['type'] != 'refresh':
                error_msg = {'refresh_token': _('Token type is not refresh!')}
                raise serializers.ValidationError(error_msg)
            validated_data['payload'] = payload
        except jwt.ExpiredSignatureError:
            error_msg = {'refresh_token': _('Refresh token is expired!')}
            raise serializers.ValidationError(error_msg)
        except jwt.InvalidTokenError:
            error_msg = {'refresh_token': _('Refresh token is invalid!')}
            raise serializers.ValidationError(error_msg)

        return validated_data

    def create(self, validated_data):
        access_payload = {
            'iss': 'backend-api',
            'user_id': validated_data['payload']['user_id'],
            'exp': datetime.utcnow() + timedelta(seconds=JWT_ACCESS_TTL),
            'type': 'access',
        }
        access = jwt.encode(payload=access_payload, key=JWT_SECRET)

        refresh_payload = {
            'iss': 'backend-api',
            'user_id': validated_data['payload']['user_id'],
            'exp': datetime.utcnow() + timedelta(seconds=JWT_REFRESH_TTL),
            'type': 'refresh',
        }
        refresh = jwt.encode(payload=refresh_payload, key=JWT_SECRET)

        return {'access': access, 'refresh': refresh}
