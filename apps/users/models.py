import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    # ids
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False)
    # auth credentials
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
    # timestamps
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("create timestamp")
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("update timestamp"))
    deleted_at = models.DateTimeField(
        null=True, default=None, verbose_name=_("delete timestamp"), blank=True
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
            return f"{self.first_name.title()} {self.last_name[0].title()}"
        except:
            return self.__str__()

    @property
    def get_full_name(self):
        try:
            return f"{self.first_name.title()} {self.middle_name.title() if self.middle_name else ''} {self.last_name}"
        except ValueError:
            return self.get_short_name

    def delete(self):
        if self.is_superuser:
            raise ValidationError("Superuses are not allowed to be deleted")
        self.deleted_at = timezone.now()
        self.is_staff = False
        self.is_active = False
        self.save()
