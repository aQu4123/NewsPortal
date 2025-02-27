from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.conf import settings

from datetime import timedelta

from celery import shared_task

from .models import Post, Category


@shared_task
def weekly_news():
    week_ago = now() - timedelta(days=7)
    posts = Post.objects.filter(date_in__gte=week_ago)
    categories = set(posts.values_list('category__name', flat=True))
    subs_emails = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'weekly_news.html',
        {
            'categories': categories,
            'posts': posts,
            'link': settings.SITE_URL,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subs_emails,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def notify_about_new_post(pk):
    post = Post.objects.get(pk=pk)
    categories = post.category.all()
    flag = [] # чтобы избежать повтор писем с одинаковым постом(из-за кол-ва категорий)
    for category in categories:
        subscribers = category.subscribers.all()
        if subscribers.exists():
            for subscriber in subscribers:
                if not subscriber.email in flag:
                    flag.append(subscriber.email)
                    html_content = render_to_string(
                        'notify_about_new_post.html',
                        {
                            'category': category,
                            'post': post,
                            'post_url': f"{settings.SITE_URL}{post.id}"
                        }
                    )
                    post_title = post.title
                    msg = EmailMultiAlternatives(
                        subject=f"Новая статья: {post_title}",
                        body='',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[subscriber.email]
                    )
                    msg.attach_alternative(html_content, 'text/html')
                    msg.send()