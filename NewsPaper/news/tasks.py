from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post
from NewsPaper.celery import app
import time

#celery -A NewsPaper worker -l INFO
#python -m celery -A NewsPaper worker -l INFO
#celery -A NewsPaper worker --loglevel=debug --concurrency=4


@app.task
def hello():
    time.sleep(10)
    print("Hello, world!")

@app.task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)


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