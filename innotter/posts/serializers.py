from rest_framework import serializers
from posts.models import Post


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
        "content",
        )

    def create(self, validated_data):
        return Post.objects.create_post(**validated_data)