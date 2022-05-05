from django.db.models.signals import post_save
from django.dispatch import receiver # импортируем нужный декоратор
from django.core.mail import mail_managers

from .models import Article, Category

from django.core.mail import EmailMultiAlternatives  # импортируем класс для создание объекта письма с html
from django.template.loader import render_to_string
from django.shortcuts import render, reverse, redirect

from django.db.models.signals import m2m_changed
from django.contrib.auth.models import User



@receiver(post_save, sender=Article)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:

        html_content = render_to_string(
            'mail_subscribers.html',
            {
                'name': Article.name,
                'ARtext': Article.ARtext,
                'Article_pk': Article.pk,
            }
        )

        msg = EmailMultiAlternatives(
            subject=f"В категории {Category.objects.get(pk=1)} новая статья!!!",
            from_email='lebedeva316@gmail.com',
            to=['lebedeva316@yandex.ru'],
        )

        msg.attach_alternative(html_content, "text/html")

        msg.send()


@receiver(post_save, sender=User)
def hi_user(sender, instance, created, **kwargs):
    assert isinstance(created, object)
    if created:
        html_content = render_to_string(
            'new_user.html',
            {
                'user': instance.username,
            }
        )
        msg = EmailMultiAlternatives(
            subject=f"Привет!",
            body=f"Добро пожаловать!",
            from_email='lebedeva316@gmail.com',
            to=[instance.email],
        )

        msg.attach_alternative(html_content, "text/html")

        msg.send()

m2m_changed.connect(notify_subscribers, sender=Article.category)


# import pathlib
# from pathlib import Path
# @receiver(post_save, sender=Article)
# def notify_subscribers(sender, instance, created, **kwargs):
#
#     if created:
#         path = pathlib.Path('c:/', 'Users', 'Анастасия Лебедева', 'Desktop', 'Python', 'project_dir2', 'project', 'db.sqlite3')
#
#         sqlite_connection = sqlite3.connect(path)
#
#         cursor = sqlite_connection.cursor()
#
#         print("Подключен")
#
#         sqlite_select_query = ("SELECT * FROM news_category_subscribers where category_id=3", (id,))
#         print("Подключен")
#         cursor.execute(sqlite_select_query)
#         print("Подключен")
#         records = cursor.fetchall()
#
#         for row in records:
#
#             first = row[2]
#
#             for User in User(user_id=first):
#                 html_content = render_to_string(
#                     'BMBNVGH.html',
#                     {
#                         'name': article.name[:30],
#                         'ARtext': article.ARtext[:30],
#                         'article_pk': article.pk
#                     }
#                 )
#
#                 msg = EmailMultiAlternatives(
#                     subject=f"В категории {Category.objects.get(pk=c.pk)} новая статья!!!",
#                     from_email='lebedeva316@gmail.com',
#                     to=['lebedeva316@yandex.ru'],
#                 )
#
#                 msg.attach_alternative(html_content, "text/html")
#
#                 msg.send()