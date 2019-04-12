from django.shortcuts import render
from .models import ProductCategory
from .models import SubCategory
from .models import Product
from basketapp.models import Basket
import random

# Названия страниц для title и названия в меню
name_main = 'Главная'
name_products = 'Товары'
name_contacts = 'Контакты'
name_categories = 'Категории'

# Состав главного меню
links_main_menu = (
    {'href': 'index', 'name': name_main},
    {'href': 'products:index', 'name': name_products},
    {'href': 'contacts', 'name': name_contacts},
)


def get_basket(request):
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
        basket.sum = 0
        for item in basket:
            basket.sum += item.product_cost
    return basket


def common_content(request):
    content = {'links_main_menu': links_main_menu,
               'basket': get_basket(request)
               }
    return content


def get_hot_product(**kwargs):
    if 'category' in kwargs:
        _products = Product.objects.filter(subcategory__category_id=kwargs['category'])
    elif 'subcategory' in kwargs:
        _products = Product.objects.filter(subcategory_id=int(kwargs['subcategory']))
    else:
        _products = Product.objects.all()

    return random.sample(list(_products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(subcategory=hot_product.subcategory). \
                        exclude(pk=hot_product.pk)[:3]

    return same_products


def main(request):
    content = {
        **common_content(request),
        'title': name_main,
    }
    return render(request, 'mainapp/index.html', content)


def categories(request):
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    categories_list = ProductCategory.objects.all()
    content = {
        **common_content(request),
        'title': name_categories,
        'items_list': categories_list,
        'menu_categories_list': categories_list,
        'hot_product': hot_product,
        'same_products': same_products,
        'type': 'categories',
    }
    return render(request, 'mainapp/categories.html', content)


def subCategories(request, cat_id):
    hot_product = get_hot_product(category=cat_id)
    same_products = get_same_products(hot_product)
    categories_list = ProductCategory.objects.all()
    subcategories_list = SubCategory.objects.filter(category=cat_id)
    content = {
        **common_content(request),
        'title': name_categories,
        'items_list': subcategories_list,
        'menu_categories_list': categories_list,
        'menu_subcategories_list': subcategories_list,
        'hot_product': hot_product,
        'same_products': same_products,
        'cat_id': int(cat_id),
        'type': 'subCategories',
    }
    return render(request, 'mainapp/categories.html', content)


def productsOfCategory(request, cat_id, scat_id):
    hot_product = get_hot_product(subcategory=scat_id)
    same_products = get_same_products(hot_product)
    categories_list = ProductCategory.objects.all()
    subcategories_list = SubCategory.objects.filter(category=scat_id)
    products_list = Product.objects.filter(subcategory=scat_id)
    content = {
        **common_content(request),
        'title': name_categories,
        'items_list': products_list,
        'menu_categories_list': categories_list,
        'menu_subcategories_list': subcategories_list,
        'cat_id': int(cat_id),
        'subcategory_id': int(scat_id),
        'hot_product': hot_product,
        'same_products': same_products,
        'type': 'productsOfCategory',
    }
    return render(request, 'mainapp/categories.html', content)


def products(request, product_id):
    product_item = Product.objects.get(pk=product_id)
    categories_list = ProductCategory.objects.all()
    subcategories_list = SubCategory.objects.filter(category=product_item.subcategory.category)
    cat_id = product_item.subcategory.category.id
    subcategory_id = product_item.subcategory.id
    content = {
        **common_content(request),
        'title': name_products,
        'product': product_item,
        'menu_categories_list': categories_list,
        'menu_subcategories_list': subcategories_list,
        'cat_id': int(cat_id),
        'subcategory_id': int(subcategory_id),
        'type': 'products',
    }

    return render(request, 'mainapp/products.html', content)


def contacts(request):
    content = {
        **common_content(request),
        'title': name_contacts,
    }
    return render(request, 'mainapp/contacts.html', content)
