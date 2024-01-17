import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from apps.base.models import BaseModel

from .managers import CustomUserManager


def filename_to_uuid(instance, filename):
    """генерация уникального имени файла"""
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"avatars/{filename}"


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    """модель пользователя"""

    email = models.EmailField(
        max_length=100, verbose_name="email", unique=True, db_index=True, null=False
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # TODO: подумать как обыграть юзернеймы... или просто выводить первую часть почты?
    username = models.CharField(unique=True, max_length=100, blank=True)

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

    avatar = models.ImageField(
        upload_to=filename_to_uuid,
        null=True,
        blank=True,
        verbose_name="Фото профиля",
        # default="avatars/default.png", закинуть картинку...
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "пользователя"
        verbose_name_plural = "пользователи"
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.last_name} {f'{self.first_name[0]}.' if self.first_name else ''} {f'{self.middle_name[0]}.' if self.middle_name else ''}".strip()

    def get_full_name(self):
        """возвращает полное имя пользователя"""
        return f"{self.first_name} {self.middle_name} {self.last_name}".strip()

    def get_tests(self):
        """возвращет все тесты пользователя"""
        return self.tests.filter(deleted_at__isnull=True)

    def get_public_tests(self):
        """возвращает все публичные тесты пользователя"""
        return self.tests.filter(is_published=True, deleted_at__isnull=True)

    def get_assigned_to_tests(self):
        """возвращает тесты которые назначили пользователю"""
        return self.assigned_to_tests.filter(deleted_at__isnull=True)

    def get_assigned_by_tests(self):
        """возвращает тесты которые назначил пользователь"""
        return self.assigned_by_tests.filter(deleted_at__isnull=True)

    def delete(self):
        """выполняет мягкое удаление пользователя и зависимых моделей (например, тесты)"""
        if self.is_superuser:
            raise ValidationError("Администратор не может быть удален")
        self.deleted_at = timezone.now()
        self.is_staff = False
        self.is_active = False
        self.save()
        # вызываем delete на каждом из тестов, если они есть
        # делаем именно через цикл, потому что для моделей прописан кастомный delete (согл. документации)
        tests = self.get_tests()
        if tests:
            for test in tests:
                test.delete()
