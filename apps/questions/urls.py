from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.QuestionCreate.as_view(), name="question-create"),
    path("<str:id>/update", views.QuestionUpdate.as_view(), name="question-update"),
    path("<str:id>/delete", views.QuestionDelete.as_view(), name="question-delete"),
    # path("<str:id>", views.QuestionDetail.as_view(), name="question-detail"),
]
