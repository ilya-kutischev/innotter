from rest_framework import serializers
from pages.models import Page
from tags.models import Tag


class PageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = "__all__"


class CreatePageSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Page
        fields = (
            'name',
            'uuid',
            'description',
            # 'followers',
            'image',
            'is_private',
            # 'follow_requests',
            'unblock_date',
            'tags',
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


class ListFollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = (
            'followers',
        )


class ListFollowRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = (
            'follow_requests',
        )


class AllowFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields=(
            'followers',
            'follow_requests',
        )

    def update(self, validated_data):
        return Page.objects.apply_all_follow_requests(**validated_data)
