from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField

from api.models import Recipe
from api.utils.serializer_utils import (
    LIMIT_NUMBER_NESTED_RECIPES,
    request_user_guard_block,
)
from .models import User, Subscribtion
from .utils.serializers_utils import BASE_FIELDS_SET_USER


class UserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания Пользователей."""

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = BASE_FIELDS_SET_USER + ("password",)


class CurrentUserSerializer(UserSerializer):
    """Сериализатор для отображения текущего пользователя."""

    class Meta(UserSerializer.Meta):
        model = User
        fields = BASE_FIELDS_SET_USER


class UserSerializer(UserSerializer):
    """Сериализатор для отображения пользователей и информации о подписках."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = BASE_FIELDS_SET_USER + ("is_subscribed",)

    def get_is_subscribed(self, obj):
        """Получение инофрмаии о подписках."""
        # request_user_guard_block
        user, guard = request_user_guard_block(self)
        return (
            guard
            and Subscribtion.objects.filter(
                user=user,
                author=obj.id,
            ).exists()
        )


class CropRecipeSerializer(serializers.ModelSerializer):
    """Сокращеный сериализатор рецептов."""

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")
        read_only_fields = fields


class SubscribtionSerializer(serializers.ModelSerializer):
    """Сериализатор Для создания и отображения подписок."""

    id = serializers.ReadOnlyField(source="author.id")
    email = serializers.ReadOnlyField(source="author.email")
    username = serializers.ReadOnlyField(source="author.username")
    first_name = serializers.ReadOnlyField(source="author.first_name")
    last_name = serializers.ReadOnlyField(source="author.last_name")
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscribtion
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def get_is_subscribed(self, obj):
        """Получение информации о подписках."""
        user, guard = request_user_guard_block(self)
        return (
            guard
            and Subscribtion.objects.filter(
                user=obj.user,
                author=obj.author,
            ).exists()
        )

    def get_recipes(self, obj):
        """Получение рецептов."""

        request = self.context.get("request")
        limit = request.query_params.get(
            "recipe_limit",
            default=LIMIT_NUMBER_NESTED_RECIPES,
        )
        queryset = Recipe.objects.filter(author=obj.author)[: int(limit)]
        return CropRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        """Получение количества рецептов."""

        return Recipe.objects.filter(author=obj.author).count()
