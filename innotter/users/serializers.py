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
        fields = "__all__"


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


class RefreshSerializer(serializers.ModelSerializer):
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


# СЕРИАЛИЗАТОР ПРИ АУТЕНТИФИКАЦИИ
class UserSerializer(serializers.ModelSerializer):
    """Ощуществляет сериализацию и десериализацию объектов User."""

    # Пароль должен содержать от 8 до 128 символов. Это стандартное правило. Мы
    # могли бы переопределить это по-своему, но это создаст лишнюю работу для
    # нас, не добавляя реальных преимуществ, потому оставим все как есть.
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'password',
            'token',
        )

        # Параметр read_only_fields является альтернативой явному указанию поля
        # с помощью read_only = True, как мы это делали для пароля выше.
        # Причина, по которой мы хотим использовать здесь 'read_only_fields'
        # состоит в том, что нам не нужно ничего указывать о поле. В поле
        # пароля требуются свойства min_length и max_length,
        # но это не относится к полю токена.
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        """Выполняет обновление User."""

        # В отличие от других полей, пароли не следует обрабатывать с помощью
        # setattr. Django предоставляет функцию, которая обрабатывает пароли
        # хешированием и 'солением'. Это означает, что нам нужно удалить поле
        # пароля из словаря 'validated_data' перед его использованием далее.
        password = validated_data.pop('password', None)

        for key, value in validated_data.items():
            # Для ключей, оставшихся в validated_data мы устанавливаем значения
            # в текущий экземпляр User по одному.
            setattr(instance, key, value)

        if password is not None:
            # 'set_password()' решает все вопросы, связанные с безопасностью
            # при обновлении пароля, потому нам не нужно беспокоиться об этом.
            instance.set_password(password)

        # После того, как все было обновлено, мы должны сохранить наш экземпляр
        # User. Стоит отметить, что set_password() не сохраняет модель.
        instance.save()

        return instance
