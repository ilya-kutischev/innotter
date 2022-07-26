from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
)
from authentication.backends import JWTAuthentication
from pages.models import Page
from pages.serializers import (
    PageDetailSerializer,
    CreatePageSerializer,
)


class PageViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = Page.objects.all()
        serializer = PageDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CreatePageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class MyPagesViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = Page.objects.filter(owner=request.user.pk)
        serializer = PageDetailSerializer(queryset, many=True)
        return Response(serializer.data)


class CreatePageView(ViewSet):
    authentication_classes = (JWTAuthentication,)
    serializer_class = CreatePageSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        serializer = CreatePageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # true
        (
            name,
            uuid,

        ) = (
            serializer.validated_data["name"],
            serializer.validated_data["uuid"],

        )
        page = Page.objects.create_page(
            name,
            request.user,
            uuid,

        )

        return Response(PageDetailSerializer(page).data)
