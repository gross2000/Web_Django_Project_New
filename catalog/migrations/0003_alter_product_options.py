# Generated by Django 5.1 on 2024-10-25 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0002_alter_version_product"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={
                "ordering": ["name", "category"],
                "permissions": [
                    ("can_edit_status", "Can edit status"),
                    ("can_edit_description", "Can edit description"),
                    ("can_edit_category", "Can edit category"),
                ],
                "verbose_name": "Продукт",
                "verbose_name_plural": "Продукты",
            },
        ),
    ]