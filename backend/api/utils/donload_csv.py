import csv
from django.http import HttpResponse
from api.models import IngredientAmount, Ingredient
from django.db.models import Sum


def generate_csv_data(request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="data.csv"'
    writer = csv.writer(response)
    writer.writerow(["Продукты", "Количество", "Еденица измерения"])
    recipes = [obj.recipe.name for obj in queryset]
    ingredients_amount = (
        IngredientAmount.objects.filter(
            recipe__name__in=recipes,
        )
        .distinct()
        .values("ingredient_id")
        .annotate(Sum("amount"))
    )
    print(ingredients_amount)
    for obj in ingredients_amount:
        writer.writerow(
            [
                Ingredient.objects.get(pk=obj["ingredient_id"]).name,
                obj["amount__sum"],
                Ingredient.objects.get(
                    pk=obj["ingredient_id"]
                ).measurement_unit,
            ]
        )
    return response
