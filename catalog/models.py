from django.conf import settings
from django.contrib.auth import get_user_model
from email.policy import default
from django.db import models
from django.contrib.auth.models import User


NULLABLE = {"blank": True, "null": True}


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="наименование категории")
    description = models.CharField(max_length=100, verbose_name="описание категории")

    def __str__(self):
        return f"{self.name} {self.description}"

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ("name",)


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name="наименование товара")
    description = models.CharField(max_length=100, verbose_name="описание товара")
    preview = models.ImageField(
        upload_to="pictures/", verbose_name="фото товара", **NULLABLE
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="категория",
        help_text="Укажите категорию товара", **NULLABLE,
        related_name="products",
    )
    price = models.FloatField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    User = get_user_model()  # Получаем текущую модель пользователя
    user = models.ForeignKey(User, verbose_name="Пользователь", blank=True, null=True, on_delete=models.SET_NULL)

    status = models.BooleanField(default=False,blank=True,null=True)


    def __str__(self):
        return f"{self.name} {self.description}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name", "category", 'price', 'created_at']
        permissions = [
            ("can_change_status", "Can change status"),
            ("can_edit_description", "Can edit description"),
            ("can_edit_category", "Can edit category"),
        ]


class Version(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    product = models.ForeignKey(
        Product,
        related_name="versions",
        on_delete=models.CASCADE,
        verbose_name="продукт",
        help_text="Укажите товар", **NULLABLE,
        )
    number = models.FloatField()
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'



class Blog(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Заголовок",
        help_text="Введите заголовок статьи",
    )
    text = models.TextField(
        verbose_name="Текст статьи", help_text="Введите текст статьи"
    )
    image = models.ImageField(
        upload_to="pictures/",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Загрузите изображение",
    )
    category = models.CharField(
        verbose_name="Признак публикации",
        help_text="Введите признак публикации",
        blank=True,
        null=True,
    )
    created_at = models.DateField(
        blank=True, null=True, verbose_name="Дата создания записи"
    )
    updated_at = models.DateField(
        blank=True, null=True, verbose_name="Дата изменения записи"
    )

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["title", "category", "created_at", "updated_at"]

    def __str__(self):
        return self.title