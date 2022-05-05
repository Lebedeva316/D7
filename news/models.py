from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(
        max_length=50,
        unique=True,
    )

    count_post = models.IntegerField(default=0, null=True, blank=True)

    is_blocked = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.name.title()

    def counter(self):
        self.count_post += 1
        self.save()
        if(self.count_post == 3):
            self.is_blocked = True
            self.save()



class Category(models.Model):

    name = models.CharField(
        max_length=50,
        unique=True,
    )

    subscribers = models.ManyToManyField(User, related_name='subscriber')

    def __str__(self):
        return self.name.title()




class Article(models.Model):

    name = models.CharField(
        max_length=50,
        unique=True,
    )
    ARtext = models.TextField()

    data = models.DateTimeField()

    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    # category = models.ManyToManyField(Category, through='ArticleCategory')


    def __str__(self):
        return f'{self.name}: {self.ARtext}'

    def get_absolute_url(self):
        return f'/news/{self.id}'



class ArticleCategory(models.Model):

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

# class Subscriber(models.Model):
#     name = models.TextField()
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     subscriber = models.ForeignKey(Category, on_delete=models.CASCADE)
#


# class AUser(models.Model):
#
#     AuthorUser = models.OneToOneField(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.name.title()
#
#     def get_absolute_url(self):
#         return f'/profile/{self.id}'


