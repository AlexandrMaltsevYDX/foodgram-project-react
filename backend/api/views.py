from django.http import HttpResponse
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
from api.serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
)


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

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=["get", "delete"],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk=None):
        """Добавляет ендпоинт favorite."""

        if request.method == "GET":
            return self.add_obj(Favorite, request.user, pk)
        elif request.method == "DELETE":
            return self.delete_obj(Favorite, request.user, pk)

    @action(
        detail=True,
        methods=["get", "delete"],
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk=None):
        """Добавляет ендпоинт карзина."""

        if request.method == "GET":
            return self.add_obj(Cart, request.user, pk)
        elif request.method == "DELETE":
            return self.delete_obj(Cart, request.user, pk)

    @action(
        detail=False, methods=["get"], permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        """Добавляет ендпоинт выгрузить из карзины."""

        user = request.user.name
        response = HttpResponse(user)
        return response

    def add_obj(self, model, user, pk):
        """Добавляет рецепт в список."""
        obj, created = model.objects.get_or_create(user=user, recipe__id=pk)
        if created:
            return Response(
                {"errors": "Рецепт уже добавлен в список"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = CropRecipeSerializer(obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_obj(self, model, user, pk):
        """Удаляет рецепт из списка."""

        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"errors": "Рецепт уже удален"}, status=status.HTTP_400_BAD_REQUEST
        )
