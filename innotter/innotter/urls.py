from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('tags/', include('tags.urls')),
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('auth/', include('authentication.urls', namespace='authentication')),
    path('pages/', include('pages.urls')),
]
