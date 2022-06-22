from django_filters import FilterSet, DateFilter, CharFilter  #, ChoiceFilter
from .models import Post
from django import forms


class PostFilter(FilterSet):
    post_time_create = DateFilter(field_name='post_time_create', lookup_expr='gt', label='Опубликовано после ',
                             widget=forms.DateInput(format='%d.%m.%Y"', attrs={'type': 'date'}))
    post_title = CharFilter(label='Название', lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ['post_time_create', 'post_title', 'post_author', 'post_category']
