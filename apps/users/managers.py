from django.contrib.auth.models import UserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class CustomUserManager(UserManager):
    def validate_email(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Введите корректный адрес эл. почты")

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Введите ваш адрес эл. почты")
        else:
            self.validate_email(email)

        if not password:
            raise ValueError("Введите пароль")

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if not extra_fields.get("is_staff"):
            raise ValueError("У администратора должен быть статус is_staff=True")
        user = self.create_user(email, password, **extra_fields)
        user.save()
        return user
