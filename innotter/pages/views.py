from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from authentication.backends import JWTAuthentication
from pages.models import Page
from pages.permissions import IsUserActiveAndNotBlockedByToken, IsOwner, IsModeratorUser
from pages.serializers import (
    PageDetailSerializer,
    CreatePageSerializer,
    UpdatePageSerializer,
    DeletePageSerializer,
    BlockPageSerializer,
    ListFollowRequestsSerializer,
    ListFollowersSerializer, AllowFollowSerializer,

)
from tags.models import Tag


class PageViewSet(ViewSet):
    permission_classes = (IsAdminUser,)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def list_all_users(self, request):
        queryset = Page.objects.all()
        serializer = PageDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser])
    def create_user_admin(self, request):
        serializer = CreatePageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated, IsOwner, IsUserActiveAndNotBlockedByToken])
    def my_pages(self, request):
        queryset = Page.objects.filter(owner=request.user.pk)
        serializer = PageDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, IsUserActiveAndNotBlockedByToken])
    def create_page(self, request):
        for tag in request.data["tags"]:
            Tag.objects.create_tag(tag)

        serializer = CreatePageSerializer(data=request.data)
        serializer.is_valid(raise_exception=False)  # true
        (
            name,
            uuid,
            description,
            image,
            is_private,
            tags,
        ) = (
            serializer.validated_data["name"],
            serializer.validated_data["uuid"],
            serializer.validated_data["description"],
            serializer.validated_data["image"],
            serializer.validated_data["is_private"],
            serializer.validated_data["tags"],
        )

        page = Page.objects.create_page(
            name,
            request.user,
            uuid,
            tags,
            description,
            image,
            is_private,
        )

        page.save()

        return Response(PageDetailSerializer(page).data)

    @action(detail=True, methods=['put'],
            permission_classes=[IsAuthenticated, IsUserActiveAndNotBlockedByToken, IsOwner])
    def update_page(self, request, *args, **kwargs):
        serializer = UpdatePageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name, description, image, is_private = (
            serializer.validated_data["name"],
            serializer.validated_data["description"],
            serializer.validated_data["image"],
            serializer.validated_data["is_private"],
        )
        page = get_object_or_404(Page, uuid=kwargs['pk'])
        page = Page.objects.update_page(page, name, description, image, is_private)
        return Response(UpdatePageSerializer(page).data)

    @action(detail=True, methods=['delete'],
            permission_classes=[IsAuthenticated, IsUserActiveAndNotBlockedByToken, IsOwner])
    def delete_page(self, request, *args, **kwargs):
        page = get_object_or_404(Page, uuid=kwargs['pk'])
        page = Page.objects.delete_page(page)
        return Response(DeletePageSerializer(page).data)

    @action(detail=False, methods=['put'], permission_classes=[IsAdminUser | IsModeratorUser])
    def block_page(self, request, uuid, *args, **kwargs):
        serializer = BlockPageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        unblock_date = serializer.validated_data["unblock_date"]

        page = get_object_or_404(Page, uuid=uuid)
        page = Page.objects.block_page(page, unblock_date)
        return Response(UpdatePageSerializer(page).data)


class FollowersViewSet(ViewSet):
    authentication_classes = (JWTAuthentication,)
    serializer_class = ListFollowersSerializer
    # permission_classes = (IsAuthenticated, IsUserActiveAndNotBlockedByToken, IsOwner,)

    @action(detail=True, methods=['get'],
            permission_classes=[IsAuthenticated, IsUserActiveAndNotBlockedByToken, IsOwner, ])
    def list_followers(self, request, *args, **kwargs):
        page = get_object_or_404(Page, uuid=kwargs['pk'])
        return Response(ListFollowersSerializer(page).data)

    @action(detail=True, methods=['get'],
            permission_classes=[IsAuthenticated, IsUserActiveAndNotBlockedByToken, IsOwner, ])
    def list_follow_requests(self, request, *args, **kwargs):
        page = get_object_or_404(Page, uuid=kwargs['pk'])
        return Response(ListFollowRequestsSerializer(page).data)

    @action(detail=False, methods=['PUT'],
            permission_classes=[IsAuthenticated, IsUserActiveAndNotBlockedByToken, IsOwner, ])
    def accept_fr(self, request, *args, **kwargs):
        serializer = AllowFollowSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        page = get_object_or_404(Page, uuid=kwargs['pk'])
        page.objects.apply_all_follow_requests()
        return Response(status=status.HTTP_200_OK)



