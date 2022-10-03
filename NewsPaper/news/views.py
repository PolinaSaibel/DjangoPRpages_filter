from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import *
from .filters import PostFilter
from .forms import PostForms, ProfileForms
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from pathlib import Path
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv
from NewsPaper.settings import DEFAULT_FROM_EMAIL


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




    # #подписка на группу
    # @login_required
    # def add_subscribe(request, **kwargs):
    #     category_number = int(kwargs['pk'])
    #     Category.objects.get(pk=category_number).subscriberss.add(request.user)
    #     return redirect('/news/')
    #
    # # отписка на группу
    # @login_required
    # def delete_subscribe(request, **kwargs):
    #     category_number = int(kwargs['pk'])
    #     Category.objects.get(pk=category_number).subscriberss.remove(request.user)
    #     return redirect('/news/')

    # def post(self, request, *args, **kwargs):
    #
    #     userid = request.user
    #     postid = self.kwargs.get('pk')
    #     postcategories = Post.objects.get(pk=postid)._postcategory.all()
    #
    #     for item in postcategories:
    #         cat = Category.objects.get(name__iexact=f'{item}')
    #         subscriber = Subscribers(subscriber=userid, C=cat)
    #         subscriber.save()
    #
    #     html_content = render_to_string('mail_for_subscriber.html',
    #             {
    #                 'subcriber': subscriber,
    #                 'cat': cat,
    #             }
    #         )
    #     msg = EmailMultiAlternatives(
    #         subject=f'{request.user.username} subscribe ',
    #         body=f"u subscribe to {cat}",  # это то же, что и message
    #         from_email='masyorova@yandex.ru',
    #         to=[request.user.email], #request.user.email # это то же, что и recipients_list
    #     )
    #     msg.attach_alternative(html_content, "text/html")  # добавляем html
    #
    #     msg.send()  # отсылаем





class PostCreate(CreateView, PermissionRequiredMixin):

    model = Post
    form_class = PostForms
    template_name = 'news_edit.html'
    permission_required = ('news.add_post')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        return super().form_valid(form)

    def post(self, request):
        cat_id =request.POST["_postcategory"] #id category
        # print(cat_id)
        cat = Category.objects.get(id=cat_id).subscriberss.all() #список всех подписчиков
        # print('quertiset',cat)
        for c in cat:

            mail=c.email
            # print("mail", mail)


            html_content = render_to_string('mess_new_post.html',
                {'header': request.POST["header"],
                'category': Category.objects.get(id=request.POST["_postcategory"]).name,
                'text': request.POST["text"],
                # 'author': request.POST["PostAutor"],
                # 'name': request.user.username
            })

            msg = EmailMultiAlternatives(
                        subject=f'Статья в вашей любимой категории {Category.objects.get(id=request.POST["_postcategory"])}.',
                        from_email=DEFAULT_FROM_EMAIL,
                        to=[mail],
                    )
            msg.attach_alternative(html_content, "text/html")  # добавляем html
            msg.send()  # отсылаем
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
    # success_url = reverse_lazy('protect/index.html')

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()

        return context

