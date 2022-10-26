from datetime import datetime, timedelta
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from .models import *
from .filters import PostFilter
from .forms import PostForms, ProfileForms
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from .tasks import notify_sub_weekly

from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv
from NewsPaper.settings import DEFAULT_FROM_EMAIL
import time



def index(request):
    return render(request, 'index2.html')

class WeekView(View):
    def get(self, request):
        notify_sub_weekly.delay()
        print('celery work')
        return redirect("/")


class NewsList(ListView):
    model = Post
    ordering = '-timeCreation'
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

class PostCategory(ListView):
    model = Post
    template_name = 'news/category.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(id=self.id) #Post.objects.filter(_postcategory=Category.objects.get(id=self.kwargs.get('pk')))
        return context


    def get_queryset(self, **kwargs):
        self.id = self.kwargs.get('pk')
        print('a', self.id)
        queryset = Post.objects.filter(_postcategory=Category.objects.get(id=self.id)) # если в Post есть поле post_category
        print(queryset)
        return queryset




class PostAuthor(ListView):
    model = Post
    template_name = 'news/author.html'
    context_object_name = 'posts'
    paginate_by = 10


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = Autor.objects.get(id=self.id) #Post.objects.filter(_postcategory=Category.objects.get(id=self.kwargs.get('pk')))

        return context


    def get_queryset(self, **kwargs):
        self.id = self.kwargs.get('pk')
        print('a', self.id)
        queryset = Post.objects.filter(PostAutor=Autor.objects.get(id=self.id)) # если в Post есть поле post_category
        print(queryset)
        return queryset



class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context

@login_required
def sub_to_category(request, pk, **kwargs):

    user = request.user
    id = pk
    cat = Category.objects.get(id=id)

    if not cat.subscriberss.filter(id=user.id).exists():
        cat.subscriberss.add(user)
        html_content = render_to_string('mail_for_subscriber.html',
                                        {
                                            'user': user,
                                            'cat': cat,
                                        }
                                        )
        msg = EmailMultiAlternatives(
            subject=f'{user.username} subscribe ',
            body=f"u subscribe to {cat}",  # это то же, что и message
            from_email=DEFAULT_FROM_EMAIL,
            to=[user.email],  # request.user.email # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html

        msg.send()  # отсылаем
    return redirect("/news")

@login_required
def unsub_to_category(request, pk):
    user = request.user
    cat = Category.objects.get(id=pk)
    if cat.subscriberss.filter(id=user.id).exists():
        cat.subscriberss.remove(user)
    return redirect("/news")




class PostCreate(CreateView, PermissionRequiredMixin):

    model = Post
    form_class = PostForms
    template_name = 'news_edit.html'
    permission_required = ('news.add_post')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.PostAutor = Autor.objects.get(autorUser=self.request.user)
        self.object.save()
        return super().form_valid(form)


    def post(self, request):
        user = User.objects.get(id=request.user.id)
        author = Autor.objects.get(autorUser=user)
        d_from = datetime.now().date()
        print("dfrom", d_from)
        d_to = d_from + timedelta(days=1)
        print('dto', d_to)
        posts = Post.objects.filter(PostAutor=author, timeCreation__range=(d_from, d_to))
        print(posts)
        if len(posts) > 1000000:
            print("howmany",len(posts))
            return redirect('/limit/')
           

        # else:
    
        return super(PostCreate, self).post(self, request)




class PostDelete(DeleteView, PermissionRequiredMixin):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('newslist')
    permission_required = ('news.delete_post',)



class PostUpdate(UpdateView, PermissionRequiredMixin):
    form_class = PostForms
    model = Post
    template_name = 'news_edit.html'
    permission_required = ('news.change_post')



class ProfileUpdate(LoginRequiredMixin, UpdateView):
    form_class = ProfileForms
    model = User
    template_name = 'profil.html'


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()

        return context

