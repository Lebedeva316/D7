import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'news_every_week': {
        'task': 'news.tasks.article_week',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday')
    },
}