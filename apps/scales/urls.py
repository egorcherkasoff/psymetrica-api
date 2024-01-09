from django.urls import path
from . import views

urlpatterns = [
    path(
        "<str:test_id>/scales",
        views.TestScalesListAPIView.as_view(),
        name="test-scales",
    ),
    path(
        "<str:test_id>/scales/create",
        views.ScaleCreateAPIView.as_view(),
        name="scales-create",
    ),
    path(
        "<str:test_id>/scales/<str:id>/update",
        views.ScaleUpdateAPIView.as_view(),
        name="scales-update",
    ),
    path(
        "<str:test_id>/scales/<str:id>/delete",
        views.ScaleDestroyAPIView.as_view(),
        name="scales-delete",
    ),
]
