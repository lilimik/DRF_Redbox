from rest_framework import viewsets, generics, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from comments.serializers import CommentsSerializer, CommentCreateSerializer
from media.models import File
from posts.models import Post
from comments.models import Comment
from posts.serializers import PostsSerializer, PostsFullSerializer


def add_file_for_instance(instance, file, pk):
    new_file = File.objects.create(file=file)
    instance = instance.objects.filter(id=pk).first()
    instance.files.add(new_file)
    instance.save()
    return Response(file.name, status.HTTP_201_CREATED)


class PostsViewSet(viewsets.GenericViewSet,
                   generics.RetrieveUpdateDestroyAPIView,
                   mixins.CreateModelMixin):

    def get_serializer_class(self):
        return PostsSerializer

    def get_queryset(self):
        return Post.objects.annotate_comments_count().all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = PostsSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def add_file(self, request, pk=None):
        file = request.FILES['file']
        return add_file_for_instance(Post, file, pk)

    @action(detail=True, methods=['GET'])
    def comments(self, request, pk=None):
        queryset = Post.objects.filter(id=pk).prefetch_related('comments').first()
        serializer = PostsFullSerializer(queryset)
        return Response(serializer.data)


class CommentsViewSet(viewsets.GenericViewSet,
                      generics.UpdateAPIView,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin):

    def get_serializer_class(self):
        return CommentsSerializer

    def get_queryset(self):
        return Comment.objects.all()

    def create(self, request):
        serializer = CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['POST'])
    def add_file(self, request, pk=None):
        file = request.FILES['file']
        return add_file_for_instance(Comment, file, pk)
