from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from fg_back.pagination import DefaultPaginator
from users.serializers import CropRecipeSerializer
from api.models import Cart, Favorite, Ingredient, Recipe, Tag
from api.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from api.filters import AuthorAndTagFilter, IngredientSearchFilter
# from api.filters import IngredientSearchFilter
from api.serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
)
from .utils.donload_csv import generate_csv_data


class TagsViewSet(ReadOnlyModelViewSet):
    """Вьюсет Тэгов."""

    permission_classes = (IsAdminOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    """Вьюсет Ингредиентов."""

    permission_classes = (IsAdminOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    search_fields = ("^name",)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет Рецетов."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_class = AuthorAndTagFilter
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = DefaultPaginator

    # def get_queryset(self):
    #     queryset = self.queryset
    #     tags = self.request.query_params.getlist("tags")
    #     # tags_slugs = self.request.query_params.getlist("tags")
    #     if tags:
    #         queryset = queryset.filter(tags__slug__in=tags)

    #     author = self.request.query_params.get("author")
    #     if author:
    #         queryset = queryset.filter(author=author)

    #     if self.request.user.is_anonymous:
    #         return queryset

    #     is_in_cart: str = self.request.query_params.get("is_in_shopping_cart")
    #     if is_in_cart == "1":
    #         queryset = queryset.filter(cart__user=self.request.user)

    #     elif is_in_cart == "0":
    #         queryset = queryset.exclude(cart__user=self.request.user)

    #     is_favorit = self.request.query_params.get("is_favorited")
    #     if is_favorit == "1":
    #         queryset = queryset.filter(favorites__user=self.request.user)
    #     if is_favorit == "0":
    #         queryset = queryset.exclude(favorites__user=self.request.user)

    #     return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk=None):
        """Добавляет ендпоинт favorite."""

        if request.method == "POST":
            return self.add_obj(Favorite, request.user, pk)
        elif request.method == "DELETE":
            return self.delete_obj(Favorite, request.user, pk)

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk=None):
        """Добавляет ендпоинт карзина."""

        if request.method == "POST":
            return self.add_obj(Cart, request.user, pk)
        elif request.method == "DELETE":
            return self.delete_obj(Cart, request.user, pk)

    @action(
        detail=False, methods=["get"], permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        """Добавляет ендпоинт выгрузить из карзины."""
        list_recipes = Cart.objects.filter(user=request.user)
        return generate_csv_data(request, list_recipes)

    def add_obj(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response(
                {"errors": "Рецепт уже добавлен в список"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = CropRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_obj(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"errors": "Рецепт уже удален"}, status=status.HTTP_400_BAD_REQUEST
        )
