import csv
from django.http import HttpResponse


def generate_csv_data(request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="data.csv"'
    writer = csv.writer(response)
    writer.writerow(["Recipes"])
    for obj in queryset:
        writer.writerow([obj.recipe.name])
    return response
