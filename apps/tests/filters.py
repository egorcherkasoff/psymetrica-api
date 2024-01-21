from django_filters import rest_framework as filters
from .models import Test
from django.db.models import Q


class AuthorFilter(filters.Filter):
    """Кастомный под-фильтр для поиска по трем полям автора теста"""

    def filter(self, qs, value):
        if value:
            return qs.filter(
                Q(author__first_name__icontains=value)
                | Q(author__last_name__icontains=value)
                | Q(author__middle_name__icontains=value)
            )
        return qs


class TestFilter(filters.FilterSet):
    """Фильтр для тестов"""

    title = filters.CharFilter(lookup_expr="icontains")
    description = filters.CharFilter(lookup_expr="icontains")
    author = AuthorFilter()

    class Meta:
        model = Test
        fields = ["title", "description", "author"]
