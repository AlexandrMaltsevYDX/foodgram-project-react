from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель Юзера."""

    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    class Meta:
        ordering = ("username",)
        verbose_name = "User"
        verbose_name_plural = "Users"


class Subscribtion(models.Model):
    """Модель подписок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers",
        verbose_name="follower",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="authors",
        verbose_name="author",
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "Subscribtion"
        verbose_name_plural = "Subscribtions"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "author"],
                name="unique follow",
            )
        ]
