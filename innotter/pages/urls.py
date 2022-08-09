from django.urls import path, include
from rest_framework.routers import DefaultRouter
from pages.views import (
    PageViewSet,
)
router = DefaultRouter()
new_router = DefaultRouter()
new_router.register(r'', PageViewSet, basename='page')


urlpatterns = [
    path('', include(new_router.urls)),
    path('', include(router.urls)),
    path('page/', include('posts.urls')),
]
