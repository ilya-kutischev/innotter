from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
)

from pages.models import Page
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
    # SendFollowRequestSerializer,
)
from rest_framework import status
from authentication.backends import JWTAuthentication


class UserViewSet(ViewSet):
    permission_classes = (IsAdminUser,)
    authentication_classes = (JWTAuthentication,)

    @action(detail=False, methods=['GET'], permission_classes=[IsAdminUser])
    def list_all_users(self, request):
        queryset = User.objects.all()
        serializer = UserDetailSerializer(queryset, many=True)
        res = Response(serializer.data)  # temp
        return Response(serializer.data)

    @action(detail=False, methods=['POST'], permission_classes=[IsAdminUser])
    def create_user_by_admin(self, request):
        serializer = UserDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def register(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username, email, password = (
            serializer.validated_data["username"],
            serializer.validated_data["email"],
            serializer.validated_data["password"],
        )
        user = User.objects.create_user(username, email, password)
        return Response(UserDetailSerializer(user).data)

    @action(detail=False, methods=['PUT'],
            permission_classes=[IsUserActiveAndNotBlockedByToken, IsOwnerByToken | IsAdminUser])
    def update_user(self, request, pk, *args, **kwargs):
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

    @action(detail=False, methods=['delete'], permission_classes=[IsAuthenticated, IsOwnerByToken | IsAdminUser])
    def delete_user(self, request, *args, **kwargs):
        user = self.request.user
        user.is_active = False
        user.is_blocked = True
        user.save()
        return Response({"result": "user deleted"})

    @action(detail=False, methods=['post'], permission_classes=[IsUserActiveAndNotBlocked])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            response_data = serializer.save()
            return Response(response_data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[IsUserActiveAndNotBlocked])
    def refresh(self, request):
        serializer = RefreshSerializer(data=request.data)
        if serializer.is_valid():
            response_data = serializer.save()
            return Response(response_data)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowRequestViewSet(ViewSet):
    authentication_classes = (JWTAuthentication,)
    # serializer_class = SendFollowRequestSerializer
    permission_classes = (IsAuthenticated, IsUserActiveAndNotBlockedByToken)

    @action(detail=True, methods=['put'], permission_classes=[IsAuthenticated, IsUserActiveAndNotBlockedByToken])
    def send_follow_request(self, request, *args, **kwargs):
        uuid = kwargs['pk']
        page = get_object_or_404(Page, uuid=uuid)
        follower = request.user
        if page.is_private:
            page = Page.objects.add_follow_request(page, follower)
        else:
            page = Page.objects.add_follower(page, follower)
        return Response(status=HTTP_200_OK)

    @action(detail=True, methods=['put'], permission_classes=[IsAuthenticated, IsUserActiveAndNotBlockedByToken])
    def unfollow(self, request, *args, **kwargs):
        uuid = kwargs['pk']
        page = get_object_or_404(Page, uuid=uuid)
        follower = request.user
        Page.objects.remove_follow_request(page, follower)
        Page.objects.remove_follower(page, follower)
        return Response(status=HTTP_200_OK)
