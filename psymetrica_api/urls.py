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
    path("api/v1/auth/", include("djoser.urls")),
    path("api/v1/auth/", include("djoser.urls.jwt")),
    path("api/v1/tests/", include("apps.tests.urls")),
    path("api/v1/questions/", include("apps.questions.urls")),
]

admin.site.site_title = "Psymetrica Admin"
admin.site.index_title = "Psymetrica Admin"
admin.site.site_header = "Welcome to Psymetrica Admin"
