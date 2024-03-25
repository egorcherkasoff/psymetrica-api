from django.urls import path

from . import views

urlpatterns = [
    path("", views.PublicTestList.as_view(), name="test-list"),
    path("<str:id>", views.PublicTestDetail.as_view(), name="test-detail"),
    path("<str:id>/attempts", views.TestAttempts.as_view(), name="test-attempts"),
    path("create/", views.TestCreate.as_view(), name="test-create"),
    path("<str:id>/update", views.TestUpdate.as_view(), name="test-update"),
    path("<str:id>/delete", views.TestDelete.as_view(), name="test-delete"),
    path(
        "<str:id>/assign/",
        views.AssignTest.as_view(),
        name="test-assign",
    ),
    path(
        "<str:id>/assignments",
        views.TestAssignsList.as_view(),
        name="test-assignments",
    ),
]
