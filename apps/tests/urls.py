from django.urls import path
from . import views

urlpatterns = [path("all/", views.TestListAPIView.as_view(), name="all-tests")]
