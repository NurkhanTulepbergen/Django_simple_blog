from django.urls import path

from . import views
from .views import (
    post_list,
    post_detail,
    post_create,
    post_edit,
    post_delete,
    add_comment
)

urlpatterns = [
    path('', post_list, name='post_list'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('post/create/', post_create, name='post_create'),
    path('post/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:post_id>/delete/', post_delete, name='post_delete'),
    path('post/<int:post_id>/comment/', add_comment, name='add_comment'),
]
