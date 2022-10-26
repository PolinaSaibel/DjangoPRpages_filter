import datetime

from django.db.models.signals import post_save, m2m_changed, pre_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import EmailMultiAlternatives
from .models import *
from .tasks import notify_sub_weekly
from django.template.loader import render_to_string

@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, action,  **kwargs):
    print(' signals...', )

    if action == 'post_add':
        print('notifying subscribers from signals...', instance.id)
        for cat in instance._postcategory.all():
            print('cat', instance._postcategory.all())
            S=Subscribers.objects.filter(C=cat)
            print(S)

            for subscribe in S:
                msg = EmailMultiAlternatives(
                            subject=f'Статья в вашей любимой категории {cat}.',
                            from_email='masyorova@yandex.ru',
                            to=[subscribe.subscriber.email],
                        )
                html_content = render_to_string('mess_new_post.html',
                        {'header': instance.header,
                         'category': subscribe.C.name,
                         'text': instance.text,
                         'username': subscribe.subscriber,
                         'pk_id': instance.pk,

                    })
                msg.attach_alternative(html_content, "text/html")  # добавляем html
                msg.send()  # отсылаем
    else:
        print("kl;;;")






