import jwt

# from django.conf import settings

from rest_framework import authentication, exceptions

from innotter.settings import JWT_SECRET
from users.models import User


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request):

        request.user = None

        # 'auth_header' должен быть массивом с двумя элементами:
        # 1) именем заголовка аутентификации (Token в нашем случае)
        # 2) сам JWT, по которому мы должны пройти аутентифкацию
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            # Некорректный заголовок токена, в заголовке передан один элемент
            return None

        elif len(auth_header) > 2:
            # Некорректный заголовок токена, какие-то лишние пробельные символы
            return None

        # JWT библиотека которую мы используем, обычно некорректно обрабатывает
        # тип bytes, который обычно используется стандартными библиотеками
        # Python3 (HINT: использовать PyJWT). Чтобы точно решить это, нам нужно
        # декодировать prefix и token. Это не самый чистый код, но это хорошее
        # решение, потому что возможна ошибка, не сделай мы этого.
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            # Префикс заголовка не тот, который мы ожидали - отказ.
            return None

        # К настоящему моменту есть "шанс", что аутентификация пройдет успешно.
        # Мы делегируем фактическую аутентификацию учетных данных методу ниже.
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        """
        Попытка аутентификации с предоставленными данными. Если успешно -
        вернуть пользователя и токен, иначе - сгенерировать исключение.
        """
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms='HS256')
        except Exception:
            msg = 'Ошибка аутентификации. Невозможно декодировать токен.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'Пользователь соответствующий данному токену не найден.'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'Данный пользователь деактивирован.'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_blocked:
            msg = 'Данный пользователь заблокирован.'
            raise exceptions.AuthenticationFailed(msg)

        return (user, token)
