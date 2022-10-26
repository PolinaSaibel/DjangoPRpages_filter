# from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from NewsPaper.celery import app
import time
from datetime import datetime, timedelta
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from .models import *
from NewsPaper.settings import DEFAULT_FROM_EMAIL

#celery -A NewsPaper worker -l INFO
#python -m celery -A NewsPaper worker -l INFO
#celery -A NewsPaper worker --loglevel=debug --concurrency=4
#celery -A NewsPaper beat -l INFO



@shared_task
def notify_sub_weekly():
    d_to = datetime.now().date()
    #print("d_to", d_to)
    d_from = d_to - timedelta(days=7)
    #print('d_from', d_from)
    posts = Post.objects.filter(timeCreation__range=(d_from, d_to))
    category =Category.objects.all()
    #print(category)
    for cat in category:
        posts_cat = posts.filter(_postcategory=cat)
        cat_id = cat.id
        #print("id", cat_id)
        #print(posts_cat)
        #print(cat)
        subscribers = cat.subscriberss.all()
       #print(subscribers)
        for c in subscribers:
            mail = c.email
            #print("mail", mail)

            html_content = render_to_string('week_mess.html',{
                'category': cat,
                'posts': posts_cat,
                'cat_id': cat_id,
            })

            msg = EmailMultiAlternatives(
                subject=f'Новости в категории {cat} за последнюю неделю.',
                from_email=DEFAULT_FROM_EMAIL,
                to=[mail],
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html
            msg.send()  # отсылаем 




def get_subscribers(category):
    user_emails =[]
    for user in category.subscriberss.all():
        user_emails.append(user.email)
    return user_emails

def new_post_sub(instanse):
    template_name = 'news_edit.html'
    latest_post = instanse
    if not latest_post.isUpdated:
        for category in latest_post._postcategory.all():
            email_subject = f'New post in category: {category.name}'
            user_email = get_subscribers()
            send_emails(
                latest_post,
                category_objact=category,
                email_subject=email_subject,
                user_email=user_email
            )


