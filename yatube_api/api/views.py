from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets

from posts.models import Group, Post
from .serializers import CommentSerializer, GroupSerializer, PostSerializer

UPDATE_POST_DENIED = 'Изменение чужого поста запрещено!'
DELETE_POST_DENIED = 'Удаление чужого поста запрещено!'
UPDATE_COMMENT_DENIED = 'Изменение чужого комментария запрещено!'
DELETE_COMMENT_DENIED = 'Удаление чужого комментария запрещено!'


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.author


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthor, permissions.IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthor, permissions.IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(
            post=get_object_or_404(Post, id=self.kwargs.get('post_id')),
            author=self.request.user)

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return post.comments.all()
