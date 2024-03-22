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
        max_length=100,
        verbose_name="Адрес эл. почты",
        unique=True,
        db_index=True,
        null=False,
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="Модератор",
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name="Администратор",
    )

    name = models.CharField(
        max_length=100,
        verbose_name="Имя пользователя",
        null=True,
        blank=True,
        db_index=True,
    )

    avatar = models.ImageField(
        upload_to=filename_to_uuid,
        null=True,
        blank=True,
        verbose_name="Фото профиля",
        default="avatars/default.jpg",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "пользователя"
        verbose_name_plural = "пользователи"
        ordering = ["-updated_at"]

    def __str__(self):
        return self.name

    def get_avatar(self):
        """возвращает урл аватара пользователя"""
        return self.avatar.url if self.avatar is not None else None

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
