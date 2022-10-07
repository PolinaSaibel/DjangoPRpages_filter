from datetime import datetime, timedelta
import logging
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMultiAlternatives
import tzlocal
import zoneinfo
from django.conf import settings
from news.models import *

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from NewsPaper.settings import DEFAULT_FROM_EMAIL



logger = logging.getLogger(__name__)
###########################
#####       python manage.py runapscheduler   ###
# наша задача по выводу текста на экран
def my_job():
    d_to = datetime.now().date()
    print("d_to", d_to)
    d_from = d_to - timedelta(days=7)
    print('d_from', d_from)
    posts = Post.objects.filter(timeCreation__range=(d_from, d_to))
    category =Category.objects.all()
    #print(category)
    for cat in category:
        posts_cat = posts.filter(_postcategory=cat)
        cat_id = cat.id
        print("id", cat_id)
        #print(posts_cat)
        print(cat)
        subscribers = cat.subscriberss.all()
        print(subscribers)
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


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE) #(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger (day="*/7"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")