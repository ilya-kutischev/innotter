from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from authentication.backends import JWTAuthentication
from posts.serializers import (
CreatePostSerializer,
PostDetailSerializer
)
from posts.models import Post
from pages.models import Page


class PostsViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        serializer = PostDetailSerializer(queryset, many=True)
        return Response(serializer.data)


class MyPostsViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)
    def list(self, request, page, *args, **kwargs):
        queryset = Post.objects.filter(page=page)
        serializer = PostDetailSerializer(queryset, many=True)
        return Response(serializer.data)


class CreatePostApi(ViewSet):
    serializer_class = CreatePostSerializer
    permission_classes = (IsAuthenticated or IsAdminUser,)
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
