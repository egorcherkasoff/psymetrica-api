from django.urls import path

from . import views

urlpatterns = [
    path(
        "<str:question_id>",
        views.QuestionOptionsListAPIView.as_view(),
        name="question-options",
    ),
    path(
        "<str:question_id>/create",
        views.OptionCreateAPIView.as_view(),
        name="option-create",
    ),
    path(
        "<str:question_id>/<str:id>/update",
        views.OptionUpdateAPIView.as_view(),
        name="option-update",
    ),
    path(
        "<str:id>/delete",
        views.OptionDeleteAPIView.as_view(),
        name="option-delete",
    ),
]
