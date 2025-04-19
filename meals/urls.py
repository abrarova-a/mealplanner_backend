from django.urls import path
from .views import register_user, login_user, get_user_details


urlpatterns = [
    path('register/', register_user),
    path('login/', login_user),
    path('api/user/', get_user_details, name='get_user_details'),
]
