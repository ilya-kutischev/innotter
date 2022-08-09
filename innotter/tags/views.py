from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from tags.models import Tag
from tags.serializers import TagDetailSerializer


class TagsViewSet(ViewSet):
    permission_classes = (IsAdminUser,)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def list_all_tags(self, request):
        queryset = Tag.objects.all()
        serializer = TagDetailSerializer(queryset, many=True)
        return Response(serializer.data)