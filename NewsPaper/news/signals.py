import datetime
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from .models import Post
from django.core.mail import EmailMultiAlternatives


@receiver(m2m_changed, sender=Post.post_category.through)
def send_mail(sender, instance, action, **kwargs):
    if action == 'post_add':
        html_content = render_to_string('message_create.html', {'new_post': instance})
        post_category = instance.post_category.all()
        emails = set()
        for cat in post_category:
            emails = cat.get_emails()
        msg = EmailMultiAlternatives(
            subject=f'Привет. Есть новая  статья в твоём любимом разделе!',
            body=instance.post_text,
            from_email='alexgoldm1991@yandex.ru',
            to=emails,
        )
        msg.attach_alternative(html_content, "post_text/html")

        msg.send()


@receiver(pre_save, sender=Post)
def check_post_today(sender, instance, **kwargs):
    today_posts = Post.objects.filter(post_time_create__date=datetime.datetime.now().date())
    return len(today_posts)
