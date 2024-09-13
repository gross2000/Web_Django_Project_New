from django.contrib import admin
from catalog.models import Product, Category

# Админка для модели Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Указываем, какие поля отображать в списке
    search_fields = ('name',)       # Добавляем возможность поиска по имени категории

# Админка для модели Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')  # Отображаем необходимые поля
    list_filter = ('category',)                          # Добавляем фильтрацию по категории
    search_fields = ('name', 'description')              # Добавляем возможность поиска по имени и описанию продукта