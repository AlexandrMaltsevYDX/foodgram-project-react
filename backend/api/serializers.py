from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.models import Ingredient, IngredientAmount, Recipe, Tag
from users.serializers import UserSerializer
from .utils.serializer_utils import ingeredient_validation


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор Тэгов."""

    class Meta:
        model = Tag
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор Ингредиентов."""

    class Meta:
        model = Ingredient
        fields = "__all__"


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Сериализатор Количества ингредиентов в рецепте."""

    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = IngredientAmount
        fields = ("id", "name", "measurement_unit", "amount")
        validators = [
            UniqueTogetherValidator(
                queryset=IngredientAmount.objects.all(),
                fields=["ingredient", "recipe"],
            )
        ]


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор Рецептов."""

    image = Base64ImageField()
    tags = TagSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(
        source="ingredientamount_set",
        many=True,
        read_only=True,
        validators=[ingeredient_validation],
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def request_user_guard_block(self):
        """Guard block если request пустой, если юзер не авторизован"""
        request = self.context.get("request")
        if request and request.user.is_anonymous:
            return False, False
        return request.user, True

    def get_is_favorited(self, obj):
        """Возвращает true если рецепт в избранных рецептов пользователя."""
        user, guard = self.request_user_guard_block()
        return (
            guard
            and Recipe.objects.filter(favorites__user=user, id=obj.id).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        """Возвращает  true если рецепт в карзине."""
        user, guard = self.request_user_guard_block()

        return (
            guard
            and Recipe.objects.filter(cart__user=user, id=obj.id).exists()
        )

    def create_ingredients(self, ingredients, recipe):
        """Создает ингредиенты для рецептов с их количеством."""

        ingredient_amounts = [
            IngredientAmount(
                recipe=recipe,
                ingredient_id=ingredient.get("id"),
                amount=ingredient.get("amount"),
            )
            for ingredient in ingredients
        ]
        IngredientAmount.objects.bulk_create(ingredient_amounts)

    def create(self, validated_data):
        """создает рецепт."""

        image = validated_data.pop("image")
        ingredients_data = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(image=image, **validated_data)
        tags_data = self.initial_data.get("tags")
        recipe.tags.set(tags_data)
        self.create_ingredients(ingredients_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        """изменяет рецепт."""

        instance.image = validated_data.get("image", instance.image)
        instance.name = validated_data.get("name", instance.name)
        instance.text = validated_data.get("text", instance.text)
        instance.cooking_time = validated_data.get(
            "cooking_time", instance.cooking_time
        )
        instance.tags.clear()
        tags_data = self.initial_data.get("tags")
        instance.tags.set(tags_data)
        IngredientAmount.objects.filter(recipe=instance).all().delete()
        self.create_ingredients(validated_data.get("ingredients"), instance)
        instance.save()
        return instance
