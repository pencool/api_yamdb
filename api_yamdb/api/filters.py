from django_filters import rest_framework as filters
from reviews.models import Title


class CharFilterInFilter(filters.CharFilter, filters.BaseInFilter):
    pass


class TitleFilter(filters.FilterSet):
    genre = CharFilterInFilter(field_name='genre__slug', lookup_expr='in')
    category = CharFilterInFilter(field_name='category__slug',
                                  lookup_expr='in')
    name = CharFilterInFilter(field_name='name', lookup_expr='in')
    year = filters.NumberFilter(field_name='year', lookup_expr='exact')

    class Meta:
        model = Title
        fields = ['genre', 'category', 'name', 'year']
