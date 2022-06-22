import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'every_week_notify': {
        'task': 'news.tasks.week_send_mail_cel',
        'schedule': crontab(0, 8, day_of_week=[1]),
        'args': (),
    },
}
