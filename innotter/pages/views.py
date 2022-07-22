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
            # description,
            # owner,
            # followers,
            # image,
            # is_private,
            # follow_requests,
            # unblock_date,
        ) = (
            serializer.validated_data["name"],
            serializer.validated_data["uuid"],
            # serializer.validated_data["description"],
            # serializer.validated_data["owner"],
            # serializer.validated_data["followers"],
            # serializer.validated_data["image"],
            # serializer.validated_data["is_private"],
            # serializer.validated_data["unblock_date"],
            # serializer.validated_data["follow_requests"],
        )
        page = Page.objects.create_page(
            name,

            # description,
            # owner,
            request.user,
            uuid,
            # followers,
            # image,
            # is_private,
            # follow_requests,
            # unblock_date,
        )

        return Response(PageDetailSerializer(page).data)
