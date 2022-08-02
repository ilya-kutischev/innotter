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
            'followers',
            'image',
            'is_private',
            'follow_requests',
            'unblock_date',
        )

    def create(self, validated_data):
        return Page.objects.create_page(**validated_data)


class UpdatePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = (
            'name',
            'description',
            'image',
            'is_private',
        )

    def update(self, validated_data):
        return Page.objects.update_page(**validated_data)


class DeletePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields=(

        )

    def delete(self, validated_data):
        return Page.objects.delete_page(**validated_data)


class BlockPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = (
            'uuid',
            'unblock_date',
        )
    def update(self, validated_data):
        return Page.objects.delete_page(**validated_data)