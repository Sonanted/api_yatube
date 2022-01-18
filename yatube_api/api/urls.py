from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from .views import CommentViewSet, GroupViewSet, PostViewSet

from django.urls import include, path

router = DefaultRouter()
router.register('posts', PostViewSet, basename='post')
router.register('groups', GroupViewSet, basename='group')
router.register(
    r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
]