from django.urls import include, path
# from rest_framework.routers import DefaultRouter


# router_api_v1 = DefaultRouter()

# router_api_v1.register("users", views.UserViewSet)


urlpatterns = [
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
