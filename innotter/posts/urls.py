from django.urls import path, include
from rest_framework.routers import DefaultRouter
from posts.views import (
    CreatePostViewSet,
    PostsViewSet,
    MyPostsViewSet,
    UpdatePostViewSet,
    DeletePostViewSet,
)

router = DefaultRouter()
router.register(r'create', CreatePostViewSet, basename='create')
router.register(r'', PostsViewSet, basename='posts')
router.register(r'my_posts', MyPostsViewSet, basename='my_posts')
router.register(r'update', UpdatePostViewSet, basename='update')
router.register(r'delete', DeletePostViewSet, basename='delete')

urlpatterns = [
    path('<int:page>/posts/', include(router.urls)),  # page = uuid, pk of the pages
    ]