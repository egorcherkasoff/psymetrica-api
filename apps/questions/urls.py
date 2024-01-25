from django.urls import path

from . import views

urlpatterns = [
    # path("<str:id>", views.PublicTestList.as_view(), name="question-detail"),
    path("create/", views.QuestionCreate.as_view(), name="question-create"),
    # path("<str:id>/update", views.TestUpdate.as_view(), name="question-update"),
    # path("<str:id>/delete", views.TestDelete.as_view(), name="question-delete"),
]
