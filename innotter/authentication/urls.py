from os.path import basename

from django.urls import path, include

from authentication.views import LoginViewSet, AuthUserViewSet, UserViewSet, UserRetrieveUpdateViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', UserViewSet, basename='')
router.register(r'user', UserRetrieveUpdateViewSet, basename='')

auth_router = DefaultRouter()
auth_router.register(r'', AuthUserViewSet, basename='my_profile')
auth_router.register(r'users/login',LoginViewSet, basename='login')
app_name = 'authentication'

urlpatterns = [
    path('users/', include(router.urls)),
    path('my_profile/', include(auth_router.urls)),
]
