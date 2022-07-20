from django.urls import path, include
from rest_framework.routers import DefaultRouter
from pages.views import (
    PageViewSet,
    CreatePageView,
)

new_router = DefaultRouter()
new_router.register(r'pages', PageViewSet, basename='page')


urlpatterns = [
    path('', include(new_router.urls)),
    path('create/', CreatePageView.as_view(), name='create-page'),
]
