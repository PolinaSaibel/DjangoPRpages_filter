from django.contrib import admin
from news.models import Autor, Category, Post, Comment, PostCategory


admin.site.register(Autor)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostCategory)
