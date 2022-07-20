from rest_framework import generics
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from pages.models import Page  # , Tag, Post
from pages.serializers import (
    PageDetailSerializer,
    CreatePageSerializer,
)


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
    permission_classes = IsAuthenticated

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

        return Response(PageDetailSerializer(page).data)
