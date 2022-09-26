from django.contrib import admin
from .models import Autor, Category, Post, Comment, PostCategory, Subscribers


admin.site.register(Autor)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostCategory)
admin.site.register(Subscribers)
