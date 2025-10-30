from django.urls import path, re_path
from .user import get_user_profile, user_preferences

urlpatterns = [
    path('profile/', get_user_profile, name='user_profile'),
    path('preferences/', user_preferences, name='user_preferences'),
]
