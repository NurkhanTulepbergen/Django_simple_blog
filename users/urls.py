from django.urls import path
from .views import (
    user_registration,
    user_profile_view,
    edit_profile,
    follow_user,
    unfollow_user
)

urlpatterns = [
    path('register/', user_registration, name='user_registration'),
    path('profile/<int:user_id>/', user_profile_view, name='profile'),
    path('profile/<int:user_id>/edit/', edit_profile, name='edit_profile'),
    path('profile/<int:user_id>/follow/', follow_user, name='follow_user'),
    path('profile/<int:user_id>/unfollow/', unfollow_user, name='unfollow_user'),
]
