from celery import shared_task
import datetime
from .models import Post, Category
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


@shared_task
def send_mail_cel(my_pk):
    instance = Post.objects.get(pk=my_pk)
    html_content = render_to_string('message_create.html', {'new_post': instance, })
    category = instance.category.all()
    emails = set()
    for cat in category:
        emails |= cat.get_emails()
    msg = EmailMultiAlternatives(
        subject=f'Здравствуй. Новая статья в твоём любимом разделе! "Celery""',
        body=instance.text,
        from_email='alexgoldm1991@yandex.ru',
        to=emails,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def week_send_mail_cel():
    delta = datetime.timedelta(7)
    start_date = datetime.datetime.utcnow() - delta
    end_date = datetime.datetime.utcnow()
    posts_for_week_send = Post.objects.filter(time_create__range=(start_date, end_date))

    for cat in Category.objects.all():
        html_content = render_to_string('account/email/week_send.html', {'posts': posts_for_week_send, 'cat': cat}, )
        msg = EmailMultiAlternatives(
            subject=f'"Еженедельная рассылка на любимые категории. Celery"',
            body='',
            from_email='alexgoldm1991@yandex.ru',
            to=cat.get_emails())
        msg.attach_alternative(html_content, "text/html")
        msg.send()
