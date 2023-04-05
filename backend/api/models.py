from django.core import validators
from django.db import models

from users.models import User
from .utils.models_utils import (
    CHAR_FIELD_DEFOULT_LEN,
    MIN_COOCKING_TIME,
    MIN_INGREDIENTS_NUMBER,
    color_validation,
)


class Ingredient(models.Model):
    """Модель ингредиентов."""

    name = models.CharField(
        max_length=CHAR_FIELD_DEFOULT_LEN,
        verbose_name="Название ингредиента",
    )
    measurement_unit = models.CharField(
        max_length=CHAR_FIELD_DEFOULT_LEN,
        verbose_name="Единица измерения",
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "measurement_unit"],
                name="unique ingredient",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.measurement_unit})"


class Tag(models.Model):
    """Модель тэгов."""

    name = models.CharField(
        max_length=CHAR_FIELD_DEFOULT_LEN,
        unique=True,
        verbose_name="Название тега",
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        validators=[color_validation],
        verbose_name="Цвет в HEX",
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="Уникальный слаг",
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор рецепта",
    )
    name = models.CharField(
        max_length=CHAR_FIELD_DEFOULT_LEN,
        verbose_name="Название рецепта",
    )
    image = models.ImageField(
        upload_to="recipes/",
        verbose_name="Картинка рецепта",
    )
    text = models.TextField(
        verbose_name="Описание рецепта",
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientAmount",
        verbose_name="Ингридиенты",
        related_name="recipes",
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Теги",
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=(
            validators.MinValueValidator(
                MIN_COOCKING_TIME,
                message=f"Минимальное время - {MIN_COOCKING_TIME} минута",
            ),
        ),
        verbose_name="Время приготовления",
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"


class IngredientAmount(models.Model):
    """Модель Количества ингредиента в рецепте для связи многие ко многим ."""

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="Ингридиент",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
    )
    amount = models.PositiveSmallIntegerField(
        validators=(
            validators.MinValueValidator(
                MIN_INGREDIENTS_NUMBER,
                message="Минимальное количество ингридиентов 1",
            ),
        ),
        verbose_name="Количество",
    )

    class Meta:
        ordering = ("ingredient",)
        verbose_name = "Количество ингридиента"
        verbose_name_plural = "Количество ингридиентов"
        constraints = [
            models.UniqueConstraint(
                fields=["ingredient", "recipe"],
                name="unique ingredients recipe",
            )
        ]


class Favorite(models.Model):
    """Модель для отображения Избранных рецептов польователя."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Рецепт",
    )

    class Meta:
        ordering = ("user",)
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="unique favorite recipe for user",
            )
        ]


class Cart(models.Model):
    """Модель корзины для хранения рецептов для покупки"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name="Рецепт",
    )

    class Meta:
        ordering = ("user",)
        verbose_name = "Корзина"
        verbose_name_plural = "В корзине"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="unique cart user",
            )
        ]
