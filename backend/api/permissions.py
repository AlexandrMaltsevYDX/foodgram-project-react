from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
)


class IsOwnerOrReadOnly(BasePermission):
    """Класс ограничения доступа.
    Полный доступ для автора, для остальных на чтение.
    """

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        return request.method in SAFE_METHODS or obj.author == request.user


class IsAdminOrReadOnly(BasePermission):
    """Класс ограничени доступа.
    Только для персонала. Для остальных на чтение.
    """

    def has_permission(
        self,
        request,
        view,
    ):
        return (
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_staff
        )
