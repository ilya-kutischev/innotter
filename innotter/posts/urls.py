from django.urls import path, include
from rest_framework.routers import DefaultRouter
from posts.views import (
    PostsViewSet,
)

router = DefaultRouter()
router.register(r'', PostsViewSet, basename='posts')


urlpatterns = [
    path('<int:page>/posts/', include(router.urls)),  # page = uuid, pk of the pages
    ]