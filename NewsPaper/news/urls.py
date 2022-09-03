from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('index', index),

    path('', NewsList.as_view(), name='newslist'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('articles/create/', PostARCreate.as_view(), name='ar_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('articles/<int:pk>/edit/', PostARUpdate.as_view(), name='ar_create'),
    path('articles/<int:pk>/delete/', PostARDelete.as_view(), name='post_delete'),
    path('profile/<int:pk>/', ProfileUpdate.as_view(), name='profile_update'),
]

