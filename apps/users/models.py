import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from apps.base.models import BaseModel

from .managers import CustomUserManager


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    """модель пользователя"""

    email = models.EmailField(
        max_length=100, verbose_name="email", unique=True, db_index=True, null=False
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # личные данные пользователя
    first_name = models.CharField(
        max_length=50, verbose_name="имя", null=True, blank=True
    )
    middle_name = models.CharField(
        max_length=50, verbose_name="отчество", null=True, blank=True
    )
    last_name = models.CharField(
        max_length=50, verbose_name="фамилия", null=True, blank=True
    )
    # todo: добавить аватарки

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "пользователя"
        verbose_name_plural = "пользователи"
        ordering = ["-updated_at"]

    def __str__(self):
        return self.email.split("@")[0]

    @property
    def get_short_name(self):
        try:
            first_name = self.first_name.title()
            last_name = self.last_name.title()
        except:
            return self.__str__()
        return f"{first_name} {last_name}"

    @property
    def get_full_name(self):
        try:
            first_name = self.first_name.title()
            middle_name = self.middle_name.title()
            last_name = self.last_name.title()
        except:
            return self.get_short_name
        return f"{first_name} {middle_name} {last_name}"

    def delete(self):
        if self.is_superuser:
            raise ValidationError("Администратор не может быть удален")
        self.deleted_at = timezone.now()
        self.is_staff = False
        self.is_active = False
        self.save()
