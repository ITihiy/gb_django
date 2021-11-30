import json
from django.core.management import BaseCommand
from django.conf import settings

from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory


class Command(BaseCommand):
    def handle(self, *args, **options):
        Product.objects.all().delete()
        ProductCategory.objects.all().delete()
        with open(f'{settings.BASE_DIR}/json/products.json', encoding='utf-8') as file_in:
            json_data = json.load(file_in)
            for current in json_data:
                category, _ = ProductCategory.objects.get_or_create(name=current['category']['name'],
                                                                    description=current['category']['description'])

                Product.objects.create(category=category, name=current['name'],
                                       short_description=current['short_description'],
                                       description=current['description'])
        print(f'Created {Product.objects.count()} products in {ProductCategory.objects.count()} categories')

        shop_admin = ShopUser.objects.create_superuser(
            username='django',
            password='geekbrains',
            email='django@email.local'
        )
