from django.urls import path, include
from rest_framework.routers import DefaultRouter
from pages.views import (
    PageViewSet,
    MyPagesViewSet,
    CreatePageView,
    UpdatePageViewSet,
    DeletePageViewSet,
    BlockPageViewSet,
)
router = DefaultRouter()
router.register(r'create', CreatePageView, basename='create')

new_router = DefaultRouter()
new_router.register(r'', PageViewSet, basename='page')
new_router.register(r'my_pages', MyPagesViewSet, basename='my_pages')

delete_router = DefaultRouter()
delete_router.register(r'', DeletePageViewSet, basename='delete_page')

update_router = DefaultRouter()
update_router.register(r'', UpdatePageViewSet, basename='update_page')

block_router = DefaultRouter()
block_router.register(r'blocks', BlockPageViewSet, basename='blocks')

urlpatterns = [
    path('', include(new_router.urls)),
    path('', include(router.urls)),
    path('page/', include('posts.urls')),
    path('delete/', include(delete_router.urls)),
    path('update/<int:uuid>/', include(update_router.urls)),
    path('blocks/<int:uuid>/', include(block_router.urls)),
]
