from rest_framework import serializers
from .models import Post, History


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'content', 'user']
        read_only_fields = ['user']


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['content', 'posted_time', 'user']
        read_only_fields = ['content', 'posted_time', 'user']
