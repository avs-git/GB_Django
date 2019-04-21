from django.shortcuts import render
from .models import Category
from .models import Product
from basketapp.models import Basket
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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


def get_hot_product():
    _products = Product.objects.all()

    return random.sample(list(_products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]

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
    categories_list = Category.objects.filter(nesting_level=0).filter(is_active=True)
    content = {
        **common_content(request),
        'title': name_categories,
        'menu_categories_list': categories_list,
        'menu_subcategories_list': categories_list,
        'hot_product': hot_product,
        'same_products': same_products,
        'type': 'categories',
    }
    return render(request, 'mainapp/categories.html', content)


# def subCategories(request, cat_id):
#     hot_product = get_hot_product(category=cat_id)
#     same_products = get_same_products(hot_product)
#     categories_list = Category.objects.all()
#     subcategories_list = Category.objects.filter(category=cat_id)
#     content = {
#         **common_content(request),
#         'title': name_categories,
#         'items_list': subcategories_list,
#         'menu_categories_list': categories_list,
#         'menu_subcategories_list': subcategories_list,
#         'hot_product': hot_product,
#         'same_products': same_products,
#         'cat_id': int(cat_id),
#         'type': 'subCategories',
#     }
#     return render(request, 'mainapp/categories.html', content)


def productsOfCategory(request, cat_id, page=1):
    hot_product = get_hot_product(category=cat_id)
    same_products = get_same_products(hot_product)
    categories_list = Category.objects.filter(nesting_level=0, is_active=True)
    subcategories_list = Category.objects.filter(parent=cat_id, is_active=True)
    products_list = Product.objects.filter(category=cat_id, category__is_active=True, is_active=True)

    # Если в этой категории нет товаров, то смотрим в дочерней
    if len(products_list) == 0:
        if len(Category.objects.filter(parent=cat_id)) != 0:
            child_category = Category.objects.filter(parent=cat_id)
            for _category in child_category:
                products_list = Product.objects.filter(category=_category.pk)
    paginator = Paginator(products_list, 2)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    content = {
        **common_content(request),
        'title': name_categories,
        'items_list': products_paginator,
        'menu_categories_list': categories_list,
        'menu_subcategories_list': subcategories_list,
        'cat_id': int(cat_id),
        'hot_product': hot_product,
        'same_products': same_products,
        'type': 'productsOfCategory',
    }

    return render(request, 'mainapp/categories.html', content)


def products(request, product_id):
    product_item = Product.objects.get(pk=product_id)
    categories_list = Category.objects.filter(nesting_level=0).filter(is_active=True)
    subcategories_list = Category.objects.filter(parent=product_item.category).filter(is_active=True)
    cat_id = product_item.category.id
    content = {
        **common_content(request),
        'title': name_products,
        'product': product_item,
        'menu_categories_list': categories_list,
        'menu_subcategories_list': subcategories_list,
        'cat_id': int(cat_id),
        'type': 'products',
    }

    return render(request, 'mainapp/products.html', content)


def contacts(request):
    content = {
        **common_content(request),
        'title': name_contacts,
    }
    return render(request, 'mainapp/contacts.html', content)
