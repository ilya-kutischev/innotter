from rest_framework import serializers

from tags.models import Tag


class TagDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
