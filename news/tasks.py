import datetime
from celery import shared_task
from django.core.mail import send_mail
from .models import Article, Category, User


@shared_task
def article_now(pid):
    for cat_id in Article.objects.get(pk=pid).Category.all():
        users = Category.objects.filter(name=cat_id).values("subscribers")
        for user_id in users:
            send_mail(
                subject=f"{Article.objects.get(pk=pid).title}",
                message=f"Здравствуй, {User.objects.get(pk=user_id['subscribers']).username}."
                        f"Новая статья в твоём любимом разделе! \n"
                        f"Заголовок статьи: {Article.objects.get(pk=pid).title} \n"
                        f"Текст статьи: {Article.objects.get(pk=pid).text[:50]} \n"
                        f"Ссылка на статью: http://127.0.0.1:8000/news/{pid}",
                from_email='lebedeva316@gmail.com',
                recipient_list=[User.objects.get(pk=user_id['subscribers']).email]
            )

@shared_task
def article_week():
    startdate = datetime.date.today() - datetime.timedelta(days=6)
    article = Article.objects.filter(dateCreation__gt=startdate).values('category', 'title', 'pk')

    for cat in Category.objects.values('pk', 'name'):
        id_articles_cat = []
        for article in articles:
            if article['category'] == cat['pk']:
                id_articles_cat.append(article['pk'])
        if not id_articles_cat == []:
            for user in User.objects.values('subscribers', 'email', 'username'):
                if user['subscribers'] == cat['pk']:
                    send_mail(
                        subject=f"Еженедельная рассылка новостей!",
                        message=f"Здравствуй, {user['username']}."
                                f"Новый список статьей в твоём любимом разделе - {cat['name']}! \n"
                                f"Ссылка на статьи: http://127.0.0.1:8000/news/search?dateCreation__gt="
                                f"{startdate}&postCategory={cat['pk']}",
                        from_email='lebedeva316@gmail.com',
                        recipient_list=[user['email']]
                    )