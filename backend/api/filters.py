from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter
from django_filters import rest_framework

from api.models import Recipe, User, Tag


class IngredientSearchFilter(SearchFilter):
    """фильтрсет для Ингридиетнов.
    Фильтрация по названию ингридиента.
    """

    search_param = "name"


class AuthorAndTagFilter(FilterSet):
    """фильтрсет для Рецептов.
    Фильтрация по автору и тэгам.
    """

    tags = rest_framework.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    author = filters.ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Recipe
        fields = ("tags", "author")
