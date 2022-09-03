from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import *
from .filters import PostFilter
from .forms import PostForms, ProfileForms

from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required



def index(request):
    return render(request, 'index2.html')

class NewsList(ListView):
    model = Post
    ordering = 'header'
    template_name = 'newslist.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'


class PostCreate(CreateView, PermissionRequiredMixin):
    form_class = PostForms
    model = Post
    template_name = 'news_edit.html'
    permission_required = ('news.add_post')
    def form_valid(self, form):
        post = form.save(commit=False)
        post.Choise = 'NW'
        return super().form_valid(form)

class PostDelete(DeleteView, PermissionRequiredMixin):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('newslist')
    permission_required = ('news.delete_post',)

class PostARCreate(CreateView, PermissionRequiredMixin):
    form_class = PostForms
    model = Post
    template_name = 'news_edit.html'
    permission_required = ('news.add_post')
    def form_valid(self, form):
        post = form.save(commit=False)
        post.Choise = 'AR'
        return super().form_valid(form)


class PostARDelete(DeleteView, PermissionRequiredMixin):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('newslist')
    permission_required = ('news.delete_post',)


class PostUpdate(UpdateView, PermissionRequiredMixin):
    form_class = PostForms
    model = Post
    template_name = 'news_edit.html'
    permission_required = ('news.change_post')

class PostARUpdate(UpdateView, PermissionRequiredMixin):
    form_class = PostForms
    model = Post
    template_name = 'news_edit.html'
    permission_required = ('news.change_post')



class ProfileUpdate(LoginRequiredMixin, UpdateView):
    form_class = ProfileForms
    model = User
    template_name = 'profil.html'
    # success_url = reverse_lazy('protect/index.html')

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context

