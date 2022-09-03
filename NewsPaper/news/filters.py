# python manage.py runserver

from django_filters import FilterSet, ModelChoiceFilter, DateFilter, ChoiceFilter
# from django_filters import FilterSet, DateFilter, CharFilter
from .models import *
from django.forms.widgets import DateInput

class PostFilter(FilterSet):
    data = DateFilter(

        field_name='timeCreation',
        lookup_expr='gte',
        widget=DateInput(
            attrs={'type': 'date'}), label='сортировка по дате')

    _postcategory = ModelChoiceFilter(lookup_expr='exact', queryset=Category.objects.all(),  label='Категории')
    Choise = ChoiceFilter(choices=ARTICLEORNEWS, label='Новость или статья')


    class Meta:
        model = Post
        fields = {'header':['icontains'],
                 }





