import django.core.exceptions
from posts.models import Comment, Group, Post
from rest_framework import viewsets

from .serializers import CommentSerializer, GroupSerializer, PostSerializer

UPDATE_POST_DENIED = 'Изменение чужого поста запрещено!'
DELETE_POST_DENIED = 'Удаление чужого поста запрещено!'
UPDATE_COMMENT_DENIED = 'Изменение чужого комментария запрещено!'
DELETE_COMMENT_DENIED = 'Удаление чужого комментария запрещено!'


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise django.core.exceptions.PermissionDenied(UPDATE_POST_DENIED)
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise django.core.exceptions.PermissionDenied(DELETE_POST_DENIED)
        super(PostViewSet, self).perform_destroy(instance)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise django.core.exceptions.PermissionDenied(
                UPDATE_COMMENT_DENIED)
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise django.core.exceptions.PermissionDenied(
                DELETE_COMMENT_DENIED)
        super(CommentViewSet, self).perform_destroy(instance)

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs.get('post_id'))
