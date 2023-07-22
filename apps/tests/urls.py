from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.TestListAPIView.as_view(), name="all-tests"),
    path("create", views.TestCreateAPIView.as_view(), name="test-create"),
    path("<str:slug>/", views.TestDetailAPIView.as_view(), name="test-detail"),
    path("<str:slug>/update", views.TestUpdateAPIView.as_view(), name="test-update"),
    path("<str:slug>/delete", views.TestDestroyAPIView.as_view(), name="test-delete"),
    path("<str:slug>/questions/", include("apps.questions.urls")),
]
