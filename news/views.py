from django.shortcuts import render
from datetime import datetime

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Article, Category

# from .models import Subscriber

from .filters import ArticleFilter
from .forms import ArticleForm, UserForm

from django.contrib.auth.mixins import PermissionRequiredMixin


from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, reverse, redirect
from django.contrib.auth.decorators import login_required

from django.views.generic import TemplateView

from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст
from django.core.mail import EmailMultiAlternatives  # импортируем класс для создание объекта письма с html


class ArticleList(ListView):

    model = Article
    ordering = '-data'
    template_name = 'news.html'
    context_object_name = 'Articles'
    paginate_by = 10
    form_class=ArticleForm
    queryset = Article.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        context['filter'] = ArticleFilter(self.request.GET, queryset=self.get_queryset())

        return context


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
            form.save()

        return super().get(request, *args, **kwargs)


class ArticleDetail(DetailView):

    model = Article
    template_name = 'Article.html'
    context_object_name = 'Article'

class Search(ListView):

    model = Article
    ordering = '-data'
    template_name = 'search.html'
    context_object_name = 'search'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        context['filter'] = ArticleFilter(self.request.GET, queryset=self.get_queryset())
        return context

class ArticleDetailView(DetailView):

    context_object_name = 'Article'
    template_name = 'Article.html'
    queryset = Article.objects.all()

#дженерик для создания новостей

class Add_news(PermissionRequiredMixin, CreateView):

    permission_required = ('news.add_article',)
    form_class = ArticleForm
    template_name = 'Add_news.html'
    context_object_name = 'Article'


class Edit_news(PermissionRequiredMixin, UpdateView):

    permission_required = ('news.change_article',)
    form_class = ArticleForm
    template_name = 'Edit_news.html'
    context_object_name = 'Article'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Article.objects.get(pk=id)

class Delete_news(PermissionRequiredMixin, DeleteView):

    permission_required = ('news.delete_article',)
    template_name = 'Delete_news.html'
    success_url = '/news/news_list/'
    context_object_name = 'Article'
    queryset = Article.objects.all()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    template_name = 'Edit_profile.html'

    form_class = UserForm

    success_url = '/news/news_list/'

    def get_object(self, **kwargs):
        return self.request.user

# class SubscribeView(ListView):
#     model = Subscriber
#     template_name = 'subscribe.html'
#     context_object_name = 'subscriber'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['categories'] = Category.objects.all
#         context['subscribers'] = Subscriber.objects.all()
#         return context
#
#     def article(self,request,*args,**kwargs):
#         user = request.user
#         category = request.POST['category']
#         subscriber = Subscriber(user = user, category_id = category)
#         subscriber.save()
#
#         return super().get(request, *args, **kwargs)


@login_required
def subscribe_category(request, pk):
    if request.user not in Category.objects.get(pk=pk).subscribers.all():
        Category.objects.get(pk=pk).subscribers.add(request.user)
    return redirect(f'/news/news_list/')

@login_required
def unsubscribe_category(request, pk):
    if request.user in Category.objects.get(pk=pk).subscribers.all():
        Category.objects.get(pk=pk).subscribers.remove(request.user)
    return redirect(f'/news/news_list/')