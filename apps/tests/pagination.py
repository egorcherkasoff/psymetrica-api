from rest_framework import pagination


class TestPagination(pagination.PageNumberPagination):
    page_size = 8
