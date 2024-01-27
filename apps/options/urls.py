from django.urls import path

from . import views

urlpatterns = [
    path(
        "create/",
        views.OptionCreate.as_view(),
        name="option-create",
    ),
    path(
        "<str:id>/update",
        views.OptionUpdate.as_view(),
        name="option-update",
    ),
    path(
        "<str:id>/delete",
        views.OptionDelete.as_view(),
        name="option-delete",
    ),
]
