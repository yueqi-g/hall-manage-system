from django.urls import path, re_path
from .user import get_user_profile, user_preferences

urlpatterns = [
    re_path(r'^profile/?$', get_user_profile, name='user_profile'),
    re_path(r'^preferences/?$', user_preferences, name='user_preferences'),
]
