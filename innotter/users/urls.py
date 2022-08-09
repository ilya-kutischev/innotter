from django.urls import path, include

from users.views import  UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', UserViewSet, basename='')


new_router = DefaultRouter()

app_name = 'USER'

urlpatterns = [

    path('', include(router.urls)),
]