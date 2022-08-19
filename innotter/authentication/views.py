from rest_framework import status
from authentication.renderers import UserJSONRenderer
from users.serializers import LoginSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import User
from users.serializers import UserDetailSerializer
from rest_framework.viewsets import ViewSet

renderer_classes = (UserJSONRenderer,)


class AuthUserViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = User.objects.filter(pk=request.user.pk)
        serializer = UserDetailSerializer(queryset, many=True)  # many=True
        return Response(serializer.data)


class UserViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        queryset = User.objects.all()
        serializer = UserDetailSerializer(queryset, many=True)
        return Response(serializer.data)


class LoginViewSet(ViewSet):
    permission_classes = IsAuthenticated
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        serializer = LoginSerializer(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        serializer = UserSerializer(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
