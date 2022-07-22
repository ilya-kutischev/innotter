from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('auth/', include('authentication.urls', namespace='authentication')),
    path('pages/', include('pages.urls')),
]
