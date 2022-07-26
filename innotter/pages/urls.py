from django.urls import path, include
from rest_framework.routers import DefaultRouter
from pages.views import (
    PageViewSet,
    MyPagesViewSet,
    CreatePageView,
)
router = DefaultRouter()
router.register(r'create', CreatePageView, basename='create')


new_router = DefaultRouter()
new_router.register(r'', PageViewSet, basename='page')
new_router.register(r'my_pages', MyPagesViewSet, basename='my_pages')

urlpatterns = [
    path('', include(new_router.urls)),
    path('', include(router.urls)),
    path('page/', include('posts.urls')),
]
