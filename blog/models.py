from django.db import models

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name="заголовок")
    slug = models.CharField(max_length=150, verbose_name='идентификатор', unique=True, null=True, blank=True)
    body = models.TextField(verbose_name="содержимое")
    image = models.ImageField(
        upload_to="pitures/",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Загрузите изображение",
    )
    created_at = models.DateField(blank=True, null=True, verbose_name="Дата создания записи")
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    views_count = models.IntegerField(default=0, verbose_name="Количество просмотров")


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "статья"
        verbose_name_plural = "статьи"