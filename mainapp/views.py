from django.shortcuts import render
from .models import ProductCategory
from .models import SubCategory
from .models import Product
from basketapp.models import Basket

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
            item.sum = item.product.price * item.quantity
            basket.sum += item.sum
    return basket


def common_content(request):
    content = {'links_main_menu': links_main_menu,
               'basket': get_basket(request)
               }
    return content


def main(request):
    content = {
        **common_content(request),
        'title': name_main,
    }
    return render(request, 'mainapp/index.html', content)


def categories(request):
    categories_list = ProductCategory.objects.all()
    content = {
        **common_content(request),
        'title': name_categories,
        'items_list': categories_list,
        'menu_categories_list': categories_list,
        'type': 'categories',
    }
    return render(request, 'mainapp/categories.html', content)


def subCategories(request, cat_id):
    categories_list = ProductCategory.objects.all()
    subcategories_list = SubCategory.objects.filter(category=cat_id)
    content = {
        **common_content(request),
        'title': name_categories,
        'items_list': subcategories_list,
        'menu_categories_list': categories_list,
        'menu_subcategories_list': subcategories_list,
        'cat_id': int(cat_id),
        'type': 'subCategories',
    }
    return render(request, 'mainapp/categories.html', content)


def productsOfCategory(request, cat_id, subcat_id):
    categories_list = ProductCategory.objects.all()
    subcategories_list = SubCategory.objects.filter(category=cat_id)
    products_list = Product.objects.filter(subcategory=subcat_id)
    content = {
        **common_content(request),
        'title': name_categories,
        'items_list': products_list,
        'menu_categories_list': categories_list,
        'menu_subcategories_list': subcategories_list,
        'cat_id': int(cat_id),
        'subcat_id': int(subcat_id),
        'type': 'productsOfCategory',
    }
    return render(request, 'mainapp/categories.html', content)


def products(request, cat_id, subcat_id, product_id):
    categories_list = ProductCategory.objects.all()
    subcategories_list = SubCategory.objects.filter(category=cat_id)
    product_item = Product.objects.get(pk=product_id)
    content = {
        **common_content(request),
        'title': name_products,
        'product': product_item,
        'menu_categories_list': categories_list,
        'menu_subcategories_list': subcategories_list,
        'cat_id': int(cat_id),
        'subcat_id': int(subcat_id),
        'type': 'products',
    }

    return render(request, 'mainapp/products.html', content)


def contacts(request):
    content = {
        **common_content(request),
        'title': name_contacts,
    }
    return render(request, 'mainapp/contacts.html', content)
