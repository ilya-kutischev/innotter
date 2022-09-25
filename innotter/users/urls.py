from django.urls import path, include
from users.views import UserViewSet, FollowRequestViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', UserViewSet, basename='')
router.register(r'', FollowRequestViewSet, basename=' follow_request')


new_router = DefaultRouter()

app_name = 'USER'

urlpatterns = [

    path('', include(router.urls)),
]