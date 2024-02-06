from django_filters.rest_framework import FilterSet
from .models import Attempt


class UserAttemptFilter(FilterSet):
    """фильтр попытки по пользователю"""

    class Meta:
        model = Attempt
        fields = {
            "user": ["exact"],
        }
