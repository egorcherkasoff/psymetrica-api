from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
]

admin.site.site_title = "Psymetrica Admin"
admin.site.index_title = "Psymetrica Admin"
admin.site.site_header = "Welcome to Psymetrica Admin"
