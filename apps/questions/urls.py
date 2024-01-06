from django.urls import path

from . import views

urlpatterns = [
    path(
        "<str:test_slug>/",
        views.TestQuestionsListAPIView.as_view(),
        name="test-questions",
    ),
    path(
        "<str:test_slug>/create/",
        views.QuestionCreateAPIView.as_view(),
        name="question-create",
    ),
    path(
        "<str:test_slug>/<str:id>/update",
        views.QuestionUpdateAPIView.as_view(),
        name="question-update",
    ),
    path(
        "<str:test_slug>/<str:id>/delete",
        views.QuestionDeleteAPIView.as_view(),
        name="question-update",
    ),
]
