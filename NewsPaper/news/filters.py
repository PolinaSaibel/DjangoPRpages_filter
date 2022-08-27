# python manage.py runserver

import django_filters
# from django_filters import FilterSet, DateFilter, CharFilter
from .models import *
from django.forms.widgets import DateInput

class PostFilter(django_filters.FilterSet):
    data = django_filters.DateFilter(
        field_name='timeCreation',
        lookup_expr='gte',
        widget=DateInput(
            attrs={'type': 'date'},))

    _postcategory = django_filters.ModelChoiceFilter(lookup_expr='exact', queryset=Category.objects.all(), label='Категории')


    class Meta:
        model = Post
        fields = {'header':['icontains']
                 ,}



 # '_postcategory':['gte']


