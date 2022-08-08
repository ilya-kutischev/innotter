from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
)
from users.models import User
from users.permissions import IsUserBlocked, IsUserActiveAndNotBlocked, IsUserActiveAndNotBlockedByToken, \
    IsOwnerByToken
from users.serializers import (
    UserDetailSerializer,
    RegisterSerializer,
    UpdateSerializer,
    DeleteSerializer,
    LoginSerializer,
    RefreshSerializer,
)
from rest_framework import status


class UserViewSet(ViewSet):
    permission_classes = (IsAdminUser,)

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class RegisterViewSet(ViewSet):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username, email, password = (
            serializer.validated_data["username"],
            serializer.validated_data["email"],
            serializer.validated_data["password"],
        )
        user = User.objects.create_user(username, email, password)
        return Response(UserDetailSerializer(user).data)


class UpdateViewSet(ViewSet):
    serializer_class = UpdateSerializer
    permission_classes = (IsUserActiveAndNotBlockedByToken, IsOwnerByToken | IsAdminUser,)

    def update(self, request, pk, *args, **kwargs):
        serializer = UpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username, email, password = (
            serializer.validated_data["username"],
            serializer.validated_data["email"],
            serializer.validated_data["password"],
        )
        user = get_object_or_404(User, pk=pk)
        user = User.objects.update_user(user, username, email, password)
        return Response(UpdateSerializer(user).data)


class DeleteViewSet(ViewSet):
    serializer_class = DeleteSerializer
    permission_classes = (IsAuthenticated, IsOwnerByToken | IsAdminUser)

    def update(self, request, *args, **kwargs):
        user = self.request.user
        user.is_active = False
        user.is_blocked = True
        user.save()
        return Response({"result": "user deleted"})


class LoginView(ViewSet):
    serializer_class = LoginSerializer
    permission_classes = (IsUserActiveAndNotBlocked,)

    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            response_data = serializer.save()
            return Response(response_data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshView(ViewSet):
    serializer_class = RegisterSerializer
    permission_classes = (IsUserActiveAndNotBlocked,)

    def create(self, request):
        serializer = RefreshSerializer(data=request.data)
        if serializer.is_valid():
            response_data = serializer.save()
            return Response(response_data)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
