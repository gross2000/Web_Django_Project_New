import json
from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Загрузка данных БД из json-файла'

    def handle(self, *args, **kwargs):
        Category.objects.all().delete()
        Product.objects.all().delete()

        with open('data.json', 'r') as file:
            data = json.load(file)
            categories = [obj for obj in data if obj.get('model') == 'catalog.category']
            products = [obj for obj in data if obj.get('model') == 'catalog.product']

            for category_data in categories:
                Category.objects.create(
                    id=category_data['pk'],
                    name=category_data['fields']['name'],
                    description=category_data['fields']['description']
                )

            for product_data in products:
                category_id = product_data['fields']['category']
                category = Category.objects.get(id=category_id)

                Product.objects.create(
                    id=product_data['pk'],
                    name=product_data['fields']['name'],
                    description=product_data['fields']['description'],
                    preview=product_data['fields']['preview'],
                    category=category,
                    price=product_data['fields']['price'],
                    created_at=product_data['fields']['created_at'],
                    updated_at=product_data['fields']['updated_at']
                )

        self.stdout.write(self.style.SUCCESS('Данные загружены успешно!!!'))