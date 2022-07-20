from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('auth/', include('authentication.urls', namespace='authentication')),
    # path('api-auth/', include('rest_framework.urls')),
    path('pages/', include('pages.urls'), namespace='pages'),
]
