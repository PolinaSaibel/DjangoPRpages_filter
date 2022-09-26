from django.db.models.signals import m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_managers
from .models import *

@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == 'post_add':
        print('notifying subscribers from signals...', instance.id)
        new_post_subscription.apply_async([instance.id])
