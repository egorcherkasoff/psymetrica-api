from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="Psymetrica API",
        default_version="v1",
        description="Psymetrica это платформа для тестов по психологии",
        contact=openapi.Contact(email="example@psymetrica.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.jwt")),
    # todo привести урлы в порядок
    path(
        "api/tests/",
        include("apps.tests.urls"),
    ),
    path("api/users/", include("apps.users.urls"))
    # path("api/v1/questions/", include("apps.questions.urls")),
    # path("api/v1/options/", include("apps.options.urls")),
    # path("api/v1/scales/", include("apps.scales.urls")),
    # path("api/v1/attempts/", include("apps.attempts.urls")),
]

admin.site.site_title = "Панель администратора"
admin.site.index_title = "Панель администратора"
admin.site.site_header = "Добро пожаловать в панель администратора"
