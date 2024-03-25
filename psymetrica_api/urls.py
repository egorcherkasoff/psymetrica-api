from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Psymetrica API",
        default_version="v1",
        description="Psymetrica это платформа для тестов по психологии",
        contact=openapi.Contact(email="example@psymetrica.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    # TODO: поменять на env var
    url="http://localhost:8080",
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-docs"),
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.jwt")),
    path(
        "api/tests/",
        include("apps.tests.urls"),
    ),
    path("api/users/", include("apps.users.urls")),
    # path("api/questions/", include("apps.questions.urls")),
    # path("api/options/", include("apps.options.urls")),
    # path("api/attempts/", include("apps.attempts.urls")),
    # path("api/v1/scales/", include("apps.scales.urls")),
]

admin.site.site_title = "Панель администратора"
admin.site.index_title = "Главная"
admin.site.site_header = "Добро пожаловать в панель администратора"
