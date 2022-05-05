from django.urls import path
from .views import *
from . import views

urlpatterns = [
   path('news_list/', ArticleList.as_view()),
   path('<int:pk>', ArticleDetailView.as_view(), name='news_detail'),
   path('search/', Search.as_view()),
   path('add/', Add_news.as_view(), name='news_create'),
   path('<int:pk>/edit/', Edit_news.as_view(), name='news_edit'),
   path('<int:pk>/delete/', Delete_news.as_view(), name='news_delete'),
   path('user/', UserUpdateView.as_view(), name='profile_edit'),
   # path('subscribe/<int:id>', views.subscribe_category, name='subscribe'),
   # path('unsubscribe/<int:id>', views.unsubscribe_category, name='unsubscribe'),
   path('subscribe/<int:pk>', subscribe_category, name='subscribe'),
   path('unsubscribe/<int:pk>', unsubscribe_category, name='unsubscribe'),
   # path('subscribe/', SubscribeView.as_view(), name='subscribe'),
]
