from rest_framework import serializers
from pages.models import Page


class PageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = "__all__"


class CreatePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = (
            'name',
            'uuid',
            'description',
            # 'owner',
            'followers',
            'image',
            'is_private',
            'follow_requests',
            'unblock_date',
        )

    def create(self, validated_data):
        return Page.objects.create_page(**validated_data)
