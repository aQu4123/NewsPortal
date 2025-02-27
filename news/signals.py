from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import mail_managers, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.conf import settings

from .models import PostCategory
from .tasks import notify_about_new_post

@receiver(m2m_changed, sender=PostCategory)
def notify(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        notify_about_new_post.delay(instance.pk)  ## taska(celeri/redis) ili vse shto snizu
        # categories = instance.category.all()
        # flag = [] # чтобы избежать повтор писем с одинаковым постом(из-за кол-ва категорий)
        # for category in categories:
        #     subscribers = category.subscribers.all()
        #     if subscribers.exists():
        #         for subscriber in subscribers:
        #             if not subscriber.email in flag:
        #                 flag.append(subscriber.email)
        #                 html_content = render_to_string(
        #                     'notify_about_new_post.html',
        #                     {
        #                         'category': category,
        #                         'post': instance,
        #                         'post_url': f"{settings.SITE_URL}{instance.id}"
        #                     }
        #                 )
        #                 post_title = instance.title
        #                 msg = EmailMultiAlternatives(
        #                     subject=f"Новая статья: {post_title}",
        #                     body='',
        #                     from_email=settings.DEFAULT_FROM_EMAIL,
        #                     to=[subscriber.email]
        #                 )
        #                 msg.attach_alternative(html_content, 'text/html')
        #                 msg.send()
