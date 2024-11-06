from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


# Create your models here.

NULLABLE = {"blank": True, "null": True}


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Создает и возвращает пользователя с email и паролем."""
        if not email:
            raise ValueError('Email является обязательным')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создает и возвращает суперпользователя с email и паролем."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)



class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Ведите email")
    phone = models.CharField(
        max_length=35,
        verbose_name="Телефон",
        help_text="Ведите номер телефона",
        **NULLABLE)

    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Фото",
        help_text="Загрузите фото продукта",
        **NULLABLE
    )
    country = models.CharField(max_length=50,
        verbose_name="Страна",
        help_text="Введите страну",
        **NULLABLE
    )
    token = models.CharField(
        max_length=100,
        verbose_name="Токен",
        help_text="Введите токен",
        **NULLABLE
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email