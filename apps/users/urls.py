from django.urls import path

from . import views

urlpatterns = [
    path("<str:id>/tests", views.UserPublicTests.as_view(), name="user-public-tests"),
    path("<str:id>/all-tests", views.UserTests.as_view(), name="user-all-tests"),
    path(
        "<str:id>/tests/assigned",
        views.UserAssignedTests.as_view(),
        name="user-assigned-tests",
    ),
]
