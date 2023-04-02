from string import hexdigits
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator

CHAR_FIELD_DEFOULT_LEN = 200
MIN_COOCKING_TIME = 1
MIN_INGREDIENTS_NUMBER = 1


class ColorValidator(BaseValidator):
    """Класс валидации для цветоговго поля."""

    def __call__(self, value):
        value = value.strip(" #")
        if len(value) not in (3, 6):
            raise ValidationError(
                f"Код цвета {value} не правильной длины ({len(value)})."
            )
        if not set(value).issubset(hexdigits):
            raise ValidationError(f"{value} не шестнадцатиричное.")
