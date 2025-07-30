import json

from django.core.management.base import BaseCommand
from foodcartapp.models import Product, ProductCategory


with open('products.json', 'r') as file:
    DATA = json.load(file)


class Command(BaseCommand):
    help = 'Скачивание бургеров через файл'

    def handle(self, *args, **options):
        for burger in DATA:
            category, _created = ProductCategory.objects.get_or_create(name=burger['type'])
            product, created = Product.objects.update_or_create(
                name=burger['title'],
                category=category,
                price=burger['price'],
                image=burger['img'],
                description=burger['description']
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Добавлен: {product}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Обновлен: {product}"))
