from rest_framework import serializers

from comments.models import Comment
from posts.models import Post


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text')


class CommentCreateSerializer(serializers.ModelSerializer):
    post = serializers.SlugRelatedField(queryset=Post.objects.all(), slug_field='id')

    class Meta:
        model = Comment
        fields = ('text', 'post')
