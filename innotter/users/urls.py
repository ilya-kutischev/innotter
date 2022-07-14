# from django.contrib import admin
from django.urls import path, include
from users.views import (
    UserViewSet,
    RegisterAPIView,
    UpdateAPIView,
    DeleteAPIView,
    LoginView,
    RefreshView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('api/register/', RegisterAPIView.as_view(), name='register'),
    path('update/<int:pk>/', UpdateAPIView.as_view(), name='update-items'),
    path('delete/<int:pk>/', DeleteAPIView.as_view(), name='delete-items'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', RefreshView.as_view(), name='refresh'),
]
