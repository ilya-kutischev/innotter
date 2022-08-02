from django.urls import path, include
from users.views import (
    UserViewSet,
    RegisterViewSet,
    UpdateViewSet,
    DeleteViewSet,
    LoginView,
    RefreshView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'register', RegisterViewSet, basename='register')
router.register(r'login', LoginView, basename='login')
router.register(r'refresh', RefreshView, basename='refresh')

urlpatterns = [
    path('', include(router.urls)),
    path('update/<int:pk>/', UpdateViewSet, name='update-items'),
    path('delete/<int:pk>/', DeleteViewSet, name='delete-items'),
]
