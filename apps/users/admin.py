from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CreateUserForm, UpdateUserForm

User = get_user_model()


# Register your models here.
class AdminUser(UserAdmin):
    ordering = ["pkid"]
    model = User
    form = UpdateUserForm
    add_form = CreateUserForm
    fieldsets = (
        (
            "Данные авторизации",
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            "Личная информация",
            {"fields": ("first_name", "middle_name", "last_name")},
        ),
        ("Даты", {"fields": ("created_at", "updated_at", "deleted_at")}),
        (
            "Аттрибуты пользователя",
            {"fields": ("is_active", "is_staff", "is_superuser")},
        ),
        ("Группы", {"fields": ["groups"]}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide"),
                "fields": ("email", "password1", "password2", "is_staff"),
            },
        ),
    )
    search_fields = ["email", "first_name", "middle_name", "last_name"]
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    list_display = [
        "id",
        "email",
        "first_name",
        "middle_name",
        "last_name",
        "is_active",
        "is_staff",
    ]
    readonly_fields = ["created_at", "updated_at"]


admin.site.register(User, AdminUser)
