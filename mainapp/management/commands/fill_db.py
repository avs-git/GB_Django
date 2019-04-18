from django.core.management.base import BaseCommand
from mainapp.models import Category, Product
from authapp.models import ShopUser

import json
import os

JSON_PATH = 'mainapp/json'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):

        # КАТЕГОРИИ
        categories = load_from_json('categories')

        Category.objects.all().delete()
        for category in categories:

            if 'parent' in category:
                parent_category = Category.objects.get(name=category['parent'])
                category['parent'] = parent_category
                category['nesting_level'] = parent_category.nesting_level + 1

            new_category = Category(**category)
            new_category.save()

        # ТОВАРЫ
        products = load_from_json('products')
        Product.objects.all().delete()

        for product in products:
            category_name = product['category']
            # Получаем категорию по имени
            _category = Category.objects.get(name=category_name)
            print('*' * 50)
            print(product, category_name, category)
            print('*' * 50)
            # Заменяем название категории объектом
            product['category'] = _category
            new_product = Product(**product)
            new_product.save()

        # Создаем суперпользователя при помощи менеджера модели
        super_user = ShopUser.objects.create_superuser('django', 'django@geekshop.local', 'geekbrains', age=33)
