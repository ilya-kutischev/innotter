from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from authentication.backends import JWTAuthentication
from posts.permissions import IsOwner, IsPageOwner, IsPageBlocked
from posts.serializers import (
    CreatePostSerializer,
    PostDetailSerializer,
    UpdatePostSerializer,
)
from posts.models import Post
from pages.models import Page
from users.permissions import IsUserBlocked


class PostsViewSet(ViewSet):
    permission_classes = (IsAdminUser,)

    def list(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        serializer = PostDetailSerializer(queryset, many=True)
        return Response(serializer.data)


class MyPostsViewSet(ViewSet):
    permission_classes = (IsAuthenticated, IsOwner, IsPageOwner, ~IsPageBlocked, ~IsUserBlocked)

    def list(self, request, page, *args, **kwargs):
        queryset = Post.objects.filter(page=page)
        serializer = PostDetailSerializer(queryset, many=True)
        return Response(serializer.data)


class CreatePostViewSet(ViewSet):
    serializer_class = CreatePostSerializer
    permission_classes = (~IsPageBlocked, ~IsUserBlocked, IsPageOwner | IsAdminUser,)
    authentication_classes = (JWTAuthentication,)

    def create(self, request, page, *args, **kwargs):
        serializer = CreatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=1)
        reply_to = request.user
        (
            content,
        )=(
            serializer.validated_data['content'],
        )
        page = Page.objects.get(uuid=page)
        post = Post.objects.create_post(content, page, reply_to)
        return Response(CreatePostSerializer(post).data)


class UpdatePostViewSet(ViewSet):
    authentication_classes = (JWTAuthentication,)
    serializer_class = UpdatePostSerializer
    permission_classes = (IsAuthenticated, IsOwner, ~IsPageBlocked, ~IsUserBlocked,)

    def update(self, request, *args, **kwargs):
        serializer = UpdatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        content = serializer.validated_data['content']

        post = get_object_or_404(Post, id=kwargs["pk"])
        post = Post.objects.update_post(post, content)
        return Response(UpdatePostSerializer(post).data)


class DeletePostViewSet(ViewSet):
    authentication_classes = (JWTAuthentication,)
    serializer_class = UpdatePostSerializer
    permission_classes = (IsOwner, IsAuthenticated, ~IsPageBlocked, ~IsUserBlocked | IsAdminUser,)

    def destroy(self, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs["pk"])
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
