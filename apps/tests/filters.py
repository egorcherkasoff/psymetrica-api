from django.db.models import Q
from django_filters import rest_framework as filters

from .models import Test


class GeneralFilter(filters.Filter):
    """Кастомный под-фильтр для поиска по нескольким полям теста"""

    def filter(self, qs, value):
        if value:
            return qs.filter(
                Q(author__first_name__icontains=value)
                | Q(author__last_name__icontains=value)
                | Q(author__middle_name__icontains=value)
                | Q(title__icontains=value)
                | Q(description__icontains=value)
            )
        return qs


class TestFilter(filters.FilterSet):
    """Фильтр для тестов"""

    query = GeneralFilter()
    category = filters.CharFilter(lookup_expr="iexact")

    class Meta:
        model = Test
        fields = ["query", "category"]
