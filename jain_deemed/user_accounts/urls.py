from django.urls import path, include

from .views import UserCreateAPIView, UserLoginAPIView

app_name = 'user_accounts'

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'), 
    path('login/', UserLoginAPIView.as_view(), name='login'),
]
