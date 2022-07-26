from os.path import basename

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from posts.views import (
    CreatePostApi,
    PostsViewSet,
    MyPostsViewSet,
)

router = DefaultRouter()
router.register(r'create', CreatePostApi, basename='create')
router.register(r'', PostsViewSet, basename)
router.register(r'my_posts', MyPostsViewSet, basename)

urlpatterns = [
    path('<int:page>/posts/', include(router.urls)),  # page = uuid, pk of the pages
    ]