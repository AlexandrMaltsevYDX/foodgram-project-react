from rest_framework.pagination import PageNumberPagination


class DefaultPaginator(PageNumberPagination):
    """Класс пагинации по умолчанию."""
    page_size_query_param = "limit"
