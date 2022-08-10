from rest_framework import status
from rest_framework.decorators import action
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
    authentication_classes = (JWTAuthentication,)
    # permission_classes = (IsAdminUser,)

    @action(detail=False, methods=['GET'], permission_classes=[IsAdminUser])
    def list_posts(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        serializer = PostDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated, IsOwner, IsPageOwner, ~IsPageBlocked, ~IsUserBlocked])
    def list_my_posts(self, request, page, *args, **kwargs):
        queryset = Post.objects.filter(page=page)
        serializer = PostDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'], permission_classes=[~IsPageBlocked, ~IsUserBlocked, IsPageOwner | IsAdminUser,])
    def create_post(self, request, page, *args, **kwargs):
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

    @action(detail=True, methods=['PUT'], permission_classes=[IsAuthenticated, IsOwner, ~IsPageBlocked, ~IsUserBlocked])
    def update_post(self, request, *args, **kwargs):
        serializer = UpdatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        content = serializer.validated_data['content']

        post = get_object_or_404(Post, id=kwargs["pk"])
        post = Post.objects.update_post(post, content)
        return Response(UpdatePostSerializer(post).data)

    @action(detail=True, methods=['delete'], permission_classes=[IsOwner, IsAuthenticated, ~IsPageBlocked, ~IsUserBlocked | IsAdminUser])
    def delete_post(self, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs["pk"])
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['put'], permission_classes=[IsAuthenticated, ~IsPageBlocked, ~IsUserBlocked | IsAdminUser])
    def like_post(self,request, *args, **kwargs):

        post = get_object_or_404(Post, id=kwargs["pk"])
        liker=request.user
        Post.objects.add_like(post, liker)

        serializer = PostDetailSerializer(post, many=False)
        return Response(serializer.data)

    @action(detail=True, methods=['put'], permission_classes=[IsAuthenticated, ~IsPageBlocked, ~IsUserBlocked | IsAdminUser])
    def unlike_post(self,request, *args, **kwargs):

        post = get_object_or_404(Post, id=kwargs["pk"])
        liker=request.user
        Post.objects.remove_like(post, liker)

        serializer = PostDetailSerializer(post, many=False)
        return Response(serializer.data)
