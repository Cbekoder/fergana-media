import django_filters
from .models import Category, Article, Video, Region

class ArticleFilter(django_filters.FilterSet):
    categories = django_filters.ModelMultipleChoiceFilter(
        field_name='categories__title',
        queryset=Category.objects.all(),
        to_field_name='title',
        label='Categories'
    )

    publish = django_filters.BooleanFilter(
        field_name='publish',
        label='Publish'
    )

    region = django_filters.ModelChoiceFilter(
        queryset=Region.objects.all(),
        field_name='region__name',
        to_field_name='name',
        label='Region'
    )

    class Meta:
        model = Article
        fields = ['categories', 'publish', 'region']


class VideoFilter(django_filters.FilterSet):
    categories = django_filters.ModelMultipleChoiceFilter(
        field_name='categories__title',
        queryset=Category.objects.all(),
        to_field_name='title',
        label='Categories'
    )

    region = django_filters.ModelChoiceFilter(
        queryset=Region.objects.all(),
        field_name='region__name',
        to_field_name='name',
        label='Region'
    )

    class Meta:
        model = Video
        fields = ['categories', 'region']
