from django.contrib import admin

from .models import Cart, Favorite, Ingredient, Recipe, Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "color")


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    list_filter = ("name",)
    search_fields = ("name",)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "count_favorites", "count_ingredients")
    list_filter = (
        "name",
        "author",
        "tags",
    )
    search_fields = ("name", "tags__name", "author__username")

    def count_favorites(self, obj):
        return obj.favorites.count()

    def count_ingredients(self, obj):
        return obj.ingredients.count()


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Cart)
admin.site.register(Favorite)
