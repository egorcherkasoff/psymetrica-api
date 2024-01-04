import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseModel

from .managers import CustomUserManager


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    
    email = models.EmailField(
        max_length=100, verbose_name=_("email"), unique=True, db_index=True, null=False
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # personal information
    first_name = models.CharField(
        max_length=50, verbose_name=_("first name"), null=True, blank=True
    )
    middle_name = models.CharField(
        max_length=50, verbose_name=_("middle name"), null=True, blank=True
    )
    last_name = models.CharField(
        max_length=50, verbose_name=_("last name"), null=True, blank=True
    )
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
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
            raise ValidationError("Superuses are not allowed to be deleted")
        self.deleted_at = timezone.now()
        self.is_staff = False
        self.is_active = False
        self.save()