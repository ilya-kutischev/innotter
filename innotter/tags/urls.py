from django.urls import path, include
from tags.views import TagsViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', TagsViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls))
]