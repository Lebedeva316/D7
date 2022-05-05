from django_filters import FilterSet, DateFilter, widgets
from .models import Article
from django import forms
import django_filters

class ArticleFilter(FilterSet):

    data = django_filters.DateFilter(lookup_expr='gt', widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Article
        fields = {
            'name',
            'author',
            'data',
        }