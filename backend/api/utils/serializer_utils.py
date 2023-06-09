from rest_framework import serializers
from django.shortcuts import get_object_or_404
from ..models import Ingredient


LIMIT_NUMBER_NESTED_RECIPES = 3


def ingeredient_validation(ingredients):
    """Функция валидации ингреиентов."""

    if not ingredients:
        raise serializers.ValidationError(
            "Нужен хоть один ингридиент для рецепта"
        )
    ingredient_list = []
    for ingredient_item in ingredients:
        ingredient = get_object_or_404(Ingredient, id=ingredient_item["id"])
        if ingredient in ingredient_list:
            raise serializers.ValidationError(
                "Ингредиенты должны быть уникальными"
            )
        ingredient_list.append(ingredient)
        amount = ingredient_item["amount"]
        if int(amount) <= 0:
            raise serializers.ValidationError(
                "Количество ингредиента должно быть больше нуля!"
            )


def recipe_unic_validation_create(author, model, validated_data):
    if model.objects.filter(
        author=author,
        name=validated_data["name"],
    ).exists():
        raise serializers.ValidationError("Рецепты должны быть ункальными")


def recipe_unic_validation_update(author, model, validated_data):
    if (
        model.objects.filter(
            name=validated_data["name"],
        )
        .exclude(
            author=author,
        )
        .exists()
    ):
        raise serializers.ValidationError("Рецепты должны быть ункальными")


def request_user_guard_block(obj):
    """Guard block если request пустой, если юзер не авторизован"""
    request = obj.context.get("request")
    if request and request.user.is_anonymous:
        return False, False
    return request.user, True
