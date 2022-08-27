from django.shortcuts import render
from django.urls import reverse_lazy
from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForms

def index(request):
    return render(request, 'index.html')

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

class PostCreate(CreateView):
    form_class = PostForms
    model = Post
    template_name = 'news_edit.html'
    def form_valid(self, form):
        post = form.save(commit=False)
        post.Choise = 'NW'
        return super().form_valid(form)

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('newslist')

class PostARCreate(CreateView):
    form_class = PostForms
    model = Post
    template_name = 'news_edit.html'
    def form_valid(self, form):
        post = form.save(commit=False)
        post.Choise = 'AR'
        return super().form_valid(form)


class PostARDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('newslist')


class PostUpdate(UpdateView):
    form_class = PostForms
    model = Post
    template_name = 'news_edit.html'

class PostARUpdate(UpdateView):
    form_class = PostForms
    model = Post
    template_name = 'news_edit.html'