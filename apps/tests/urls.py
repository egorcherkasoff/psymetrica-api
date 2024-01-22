from django.urls import path

from . import views

urlpatterns = [
    path("", views.PublicTestList.as_view(), name="test-list"),
    path("<str:slug>", views.PublicTestDetail.as_view(), name="test-detail"),
    path("create/", views.TestCreate.as_view(), name="test-create"),
    path("<str:slug>/update", views.TestUpdate.as_view(), name="test-update"),
    path("<str:slug>/delete", views.TestDelete.as_view(), name="test-delete"),
    path(
        "<str:slug>/assign/",
        views.AssignTest.as_view(),
        name="test-assign",
    ),
    # перенести в apps.users
    path(
        "users/<uuid:id>/assigned/",
        views.TestsAssignedToUserListAPIView.as_view(),
        name="test-assigned-to-user",
    ),
]
