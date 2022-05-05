import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.db.models.signals import post_save
from django.dispatch import receiver
from ...models import Article, Subscriber
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render, reverse, redirect


logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    #  Your job processing logic here...
    instance = Article.objects.all().order_by('-data')[:5]
    subscribers = Subscriber.objects.all()

    for subscriber in subscribers:
        html_content = render_to_string(
            'week_article.html',
            {
                'article': instance,
                'subscriber': subscriber,
            }
        )

        msg = EmailMultiAlternatives(
            subject= f'Новые статьи за неделю',
            from_email= 'lebedeva316@gmail.com',
            to= ['lebedeva316@yandex.ru'],
        )
        msg.attach_alternative(html_content, "text/html")

        msg.send()


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")


        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")