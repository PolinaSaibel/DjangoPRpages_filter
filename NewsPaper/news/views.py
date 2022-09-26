from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import *
from .filters import PostFilter
from .forms import PostForms, ProfileForms
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv


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
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context
    # def get(self, request, *args, **kwargs):
    #     try:
    #         self.object = self.get_object()
    #     except Http404:
    #         return redirect('search')
    #     context = self.get_context_data(object=self.object)
    #     return self.render_to_response(context)

    #подписка на группу
    @login_required
    def add_subscribe(request, **kwargs):
        category_number = int(kwargs['pk'])
        Category.objects.get(pk=category_number).subscriberss.add(request.user)
        return redirect('/news/')

    # отписка на группу
    @login_required
    def delete_subscribe(request, **kwargs):
        category_number = int(kwargs['pk'])
        Category.objects.get(pk=category_number).subscriberss.remove(request.user)
        return redirect('/news/')

    def post(self, request, *args, **kwargs):

        userid = request.user
        postid = self.kwargs.get('pk')
        postcategories = Post.objects.get(pk=postid)._postcategory.all()

        for item in postcategories:
            cat = Category.objects.get(name__iexact=f'{item}')
            subscriber = Subscribers(subscriber=userid, C=cat)
            subscriber.save()

        html_content = render_to_string('mail_for_subscriber.html',
                {
                    'subcriber': subscriber,
                    'cat': cat,
                }
            )
        msg = EmailMultiAlternatives(
            subject=f'{request.user.username} subscribe ',
            body=f"u subscribe to {cat}",  # это то же, что и message
            from_email='masyorova@yandex.ru',
            to=[request.user.email], #request.user.email # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html

        msg.send()  # отсылаем

        # send_mail(
        #     subject=f'{request.user.username} subscribe ',
        #     # имя клиента и дата записи будут в теме для удобства
        #     message=f"u subscribe to {cat}",  # сообщение с кратким описанием проблемы
        #     from_email='masyorova@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
        #     recipient_list=['masyorova99@gmail.com']  # здесь список получателей. Например, секретарь, сам врач и т. д.
        # )
        return redirect('/')




class PostCreate(CreateView, PermissionRequiredMixin):
    form_class = PostForms
    model = Post
    template_name = 'news_edit.html'
    permission_required = ('news.add_post')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.Choise = 'NW'
        return super().form_valid(form)


    def post(self, request, *args, **kwargs):
        global Subscribers
        #subscriber = Subscribers.objects.filter(C=Category.objects.get(id=).subscriber.all())
        html_content = render_to_string('mess_new_post.html',
        {'header': request.POST["header"],
        'category': Category.objects.get(id=request.POST["_postcategory"]).name,
        'text': request.POST["text"],
        'author': request.POST["PostAutor"],
        'name': request.user.username
    })
        for sub in Subscribers.objects.filter(C=Category.objects.get(id=request.POST["_postcategory"])):
            msg = EmailMultiAlternatives(
                subject=f'Статья в вашей любимой категории {Category.objects.get(id=request.POST["_postcategory"])}. ' ,
                body=Post.text,  # это то же, что и message
                from_email='masyorova@yandex.ru',
                to=[sub(User.email)],  #Category.objects.get(id=request.POST["_postcategory"]).subscriberss.get(request.user.email)
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html


            msg.send()  # отсылаем
        return redirect('/')


    #
    # def new_post_subscription(oid):
    #     template = 'newpost.html'
    #     latest_pst = Post.objects.get(pk=oid)
    #     # print(latest_post)
    #     # print(f'latest_post.isUpdated = {latest_post.isUpdated}')
    #
    #     # if not latest_pst.isUpdated:
    #     # sleep(5)
    #     print(latest_pst.title)
    #     categories = latest_pst.cats.all()
    #     print(f'categories = {categories}')
    #     for category in categories:
    #         # print('do we get into for?')
    #         email_subject = f"New Post in Category: '{category}'"
    #         print(f'category = {category}')
    #         email_recipients = oid.collect_subscribers(category)
    #         print(f'new_post_subscription func collected subscribers: {email_recipients}')
    #         send_emails(
    #             latest_pst,
    #             category_object=category,
    #             email_subject=email_subject,
    #             template=template,
    #             email_recipients=email_recipients)


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

