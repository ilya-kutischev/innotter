from django.urls import path, include
from rest_framework.routers import DefaultRouter
from pages.views import (
    PageViewSet,
    MyPagesViewSet,
    CreatePageView,
    UpdatePageAPIView,
    DeletePageAPIView,
)
router = DefaultRouter()
router.register(r'create', CreatePageView, basename='create')

new_router = DefaultRouter()
new_router.register(r'', PageViewSet, basename='page')
new_router.register(r'my_pages', MyPagesViewSet, basename='my_pages')

delete_router = DefaultRouter()
delete_router.register(r'', DeletePageAPIView, basename='delete_page')

urlpatterns = [
    path('', include(new_router.urls)),
    path('', include(router.urls)),
    path('page/', include('posts.urls')),
    path('delete/', include(delete_router.urls)),
    path('update/<int:uuid>/', UpdatePageAPIView.as_view(),name='update_page'),
]
