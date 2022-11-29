from django.contrib import admin
from django.urls import path
from django.views.decorators.cache import cache_page
from .views import *

urlpatterns = [
    path('index', index),


    path('', NewsList.as_view(), name='newslist' ),

    path('', cache_page(60*2)(NewsList.as_view()), name='newslist'),#кэш главной стр

    path('week/', WeekView.as_view()),
    path('category/<int:pk>', PostCategory.as_view(), name='post_category'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('profile/<int:pk>/', ProfileUpdate.as_view(), name='profile_update'),
    path('sub/<int:pk>/', sub_to_category, name='sub_to_category'),
    path('unsub/<int:pk>', unsub_to_category, name='unsub_to_cat'),
    path('limit/', PostCreate.as_view(), name='limit'),
    path('author/<int:pk>', PostAuthor.as_view(), name='autor'),


]

