from django.urls import path

from . import views

urlpatterns = [
    path("<int:number>", views.QuestionDetailAPIView.as_view(), name="view-question"),
    path("create", views.QuestionCreateAPIView.as_view(), name="create-question"),
]
