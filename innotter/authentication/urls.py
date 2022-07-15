from django.urls import path
from users.views import RegisterAPIView
from authentication.views import LoginAPIView, UserRetrieveUpdateAPIView

# ТУТ УРЛЫ ДЛЯ АУТЕНТИФИКАЦИИ

app_name = 'authentication'
urlpatterns = [
    path('user', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegisterAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
]
