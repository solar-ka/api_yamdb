from django_filters import rest_framework as filters, ModelChoiceFilter
from reviews.models import Genre, Title, Category


class TitleFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    category = ModelChoiceFilter(
        to_field_name='slug',
        queryset=Category.objects.all()
    )
    genre = ModelChoiceFilter(
        to_field_name='slug',
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = ('name', 'year',)
