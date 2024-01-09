from django.urls import path
from . import views

urlpatterns = [
    path(
        "<str:test_id>/start", views.StartAttemptAPIView.as_view(), name="start-attempt"
    ),
    path("<str:id>", views.AttemptRetrieveAPIView.as_view(), name="attempt-view"),
    path(
        "<str:attempt_id>/answers/create",
        views.CreateAttemptAnswerCreateAPIView.as_view(),
        name="attempt-add-answer",
    ),
]
