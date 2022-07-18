# from django.shortcuts import render
from rest_framework import generics
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    # IsAuthenticatedOrReadOnly,
)

# from django.contrib.auth.decorators import login_required
from users.models import User, Page  # , Tag, Page
from users.serializers import (
    UserDetailSerializer,
    RegisterSerializer,
    UpdateSerializer,
    DeleteSerializer,
    LoginSerializer,
    RefreshSerializer,
    PageDetailSerializer,
    CreatePageSerializer,
)
from rest_framework import status


class UserViewSet(ViewSet):
    permission_classes = (AllowAny,)

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # def destroy(self, request, *args, **kwargs):
    #     user = request.user  # deleting user
    #     # you custom logic #
    #     return super(UserViewSet, self).destroy(request, *args, **kwargs)


# Register API
class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username, email, password = (
            serializer.validated_data["username"],
            serializer.validated_data["email"],
            serializer.validated_data["password"],
        )
        user = User.objects.create_user(username, email, password)
        # return user
        return Response(UserDetailSerializer(user).data)
        # return Response({
        # "user": UserDetailSerializer(user, context=self.get_serializer_context()).data,
        # "token": AuthToken.objects.create(user)[1]
        # })


# Update API
class UpdateAPIView(generics.GenericAPIView):
    serializer_class = UpdateSerializer
    permission_classes = IsAuthenticated or IsAdminUser
    # def update(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(request.user, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     username, email, password = (
    #         serializer.validated_data["username"],
    #         serializer.validated_data["email"],
    #         serializer.validated_data["password"],
    #         )
    #     user = User.objects.update_user(username, email, password, title=None)
    #     serializer.save()
    #     return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        username, email, password = (
            serializer.validated_data["username"],
            serializer.validated_data["email"],
            serializer.validated_data["password"],
        )
        user = get_object_or_404(User, pk=pk)
        user = User.objects.update_user(user, username, email, password)
        # return user
        return Response(UpdateSerializer(user).data)


class DeleteAPIView(generics.GenericAPIView):
    serializer_class = DeleteSerializer
    permission_classes = IsAuthenticated

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        user.delete()
        # ВНИМАНИЕ тут надо сделать вместо этой хуйни isblocked=true
        return Response({"result": "user deleted"})


# AUTHENTICATION ##################################
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            response_data = serializer.save()
            return Response(response_data)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = RefreshSerializer(data=request.data)
        if serializer.is_valid():
            response_data = serializer.save()
            return Response(response_data)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PageViewSet(ViewSet):
    permission_classes = (AllowAny,)

    def list(self, request):
        queryset = Page.objects.all()
        serializer = PageDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CreatePageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CreatePageView(generics.GenericAPIView):
    serializer_class = CreatePageSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        (
            name,
            uuid,
            description,
            owner,
            followers,
            image,
            is_private,
            follow_requests,
            unblock_date,
        ) = (
            serializer.validated_data["name"],
            serializer.validated_data["uuid"],
            serializer.validated_data["description"],
            serializer.validated_data["owner"],
            serializer.validated_data["followers"],
            serializer.validated_data["image"],
            serializer.validated_data["is_private"],
            serializer.validated_data["unblock_date"],
            serializer.validated_data["follow_requests"],
        )
        page = Page.objects.create_page(
            name,
            uuid,
            description,
            owner,
            followers,
            image,
            is_private,
            follow_requests,
            unblock_date,
        )

        return Response(UserDetailSerializer(page).data)
