from django.contrib import admin
from django.urls import path, include
from users.views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
]
