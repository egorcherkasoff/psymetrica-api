from rest_framework.pagination import PageNumberPagination


class QuestionPagingation(PageNumberPagination):
    page_size = 10
