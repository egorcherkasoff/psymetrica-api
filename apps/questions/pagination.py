from rest_framework.pagination import PageNumberPagination


class QuestionPagination(PageNumberPagination):
    page_size = 1
