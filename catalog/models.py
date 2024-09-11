from django.db import models

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
        help_text="Укажите категорию товара",
        **NULLABLE,
        related_name="products",
    )
    price = models.FloatField()
    created_at = models.DateField()
    updated_at = models.DateField()

    def __str__(self):
        return f"{self.name} {self.description}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name", "category"]