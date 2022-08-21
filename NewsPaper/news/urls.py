from django.contrib import admin
from django.urls import path
from news.views import index
from news.views import NewsList, PostDetail

urlpatterns = [
    path('index', index),
    path('', NewsList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
]