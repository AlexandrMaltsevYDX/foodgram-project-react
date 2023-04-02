from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from fg_back.pagination import DefaultPaginator

# from api.pagination import LimitPageNumberPagination
from .serializers import SubscribtionSerializer
from .models import Subscribtion

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Вьюсет юзера."""

    pagination_class = DefaultPaginator

    @action(detail=True, permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        """Добаление ендпоинта для подписки."""

        user = request.user
        author = get_object_or_404(User, id=id)

        if user == author:
            return Response(
                {"errors": "Вы не можете подписываться на самого себя"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if Subscribtion.objects.filter(user=user, author=author).exists():
            return Response(
                {"errors": "Вы уже подписаны на данного пользователя"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        subscribtion = Subscribtion.objects.create(user=user, author=author)
        serializer = SubscribtionSerializer(
            subscribtion, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def del_subscribe(self, request, id=None):
        """Добавление ендпоинта для удаления подписик."""

        user = request.user
        author = get_object_or_404(User, id=id)
        if user == author:
            return Response(
                {"errors": "Вы не можете отписываться от самого себя"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        subscribtion = Subscribtion.objects.filter(user=user, author=author)
        if subscribtion.exists():
            subscribtion.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {"errors": "Вы уже отписались"}, status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        """Добавление ендпоинта для просмотра подписок."""

        user = request.user
        queryset = Subscribtion.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribtionSerializer(
            pages, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)
