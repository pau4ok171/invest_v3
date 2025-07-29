from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_query_param = '_page'
    page_size_query_param = '_limit'
    max_page_size = 20
