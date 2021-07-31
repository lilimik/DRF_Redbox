from rest_framework import serializers

from comments.models import Comment
from comments.serializers import CommentsSerializer
from posts.models import Post


class PostsSerializer(serializers.ModelSerializer):
    comments_count = serializers.SerializerMethodField('get_comments_count')

    def get_comments_count(self, instance):
        return Comment.objects.filter(post=instance).count()

    class Meta:
        model = Post
        fields = ('id', 'name', 'content', 'comments_count')


class PostsFullSerializer(PostsSerializer):
    comments = CommentsSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = (*PostsSerializer.Meta.fields, 'comments')
