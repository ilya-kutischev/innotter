from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated, IsAdminUser,
)
from authentication.backends import JWTAuthentication
from pages.models import Page
from pages.permissions import IsUserActiveAndNotBlockedByToken, IsOwner, IsPageBlocked, IsModeratorUser
from pages.serializers import (
    PageDetailSerializer,
    CreatePageSerializer,
    UpdatePageSerializer,
    DeletePageSerializer, BlockPageSerializer,
)


class PageViewSet(ViewSet):
    permission_classes = (IsAdminUser,)

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
    permission_classes = (IsAuthenticated, IsOwner, IsUserActiveAndNotBlockedByToken)

    def list(self, request):
        queryset = Page.objects.filter(owner=request.user.pk)
        serializer = PageDetailSerializer(queryset, many=True)
        return Response(serializer.data)


class CreatePageView(ViewSet):
    authentication_classes = (JWTAuthentication, IsUserActiveAndNotBlockedByToken)
    serializer_class = CreatePageSerializer
    permission_classes = (IsAuthenticated, )

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


class UpdatePageViewSet(ViewSet):
    authentication_classes = (JWTAuthentication,)
    serializer_class = UpdatePageSerializer
    permission_classes = (IsAuthenticated,IsUserActiveAndNotBlockedByToken, IsOwner, not IsPageBlocked,)

    def update(self, request, uuid, *args, **kwargs):
        serializer = UpdatePageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name, description, image, is_private = (
            serializer.validated_data["name"],
            serializer.validated_data["description"],
            serializer.validated_data["image"],
            serializer.validated_data["is_private"],
        )
        page = get_object_or_404(Page, uuid=uuid)
        page = Page.objects.update_page(page, name, description, image, is_private)
        return Response(UpdatePageSerializer(page).data)


class DeletePageViewSet(ViewSet):
    authentication_classes = (JWTAuthentication,)
    serializer_class = DeletePageSerializer
    permission_classes = (IsAuthenticated, IsUserActiveAndNotBlockedByToken, IsOwner,)

    def update(self, request, *args, **kwargs):
        page = get_object_or_404(Page, uuid=kwargs['pk'])
        page = Page.objects.delete_page(page)
        return Response(DeletePageSerializer(page).data)


class BlockPageViewSet(ViewSet):
    authentication_classes = (JWTAuthentication,)
    serializer_class = BlockPageSerializer
    permission_classes = (IsAdminUser | IsModeratorUser,)

    def update(self, request, uuid, *args, **kwargs):
        serializer = BlockPageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        unblock_date = serializer.validated_data["unblock_date"]

        page = get_object_or_404(Page, uuid=uuid)
        page = Page.objects.block_page(page, unblock_date)
        return Response(UpdatePageSerializer(page).data)