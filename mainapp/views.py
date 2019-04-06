from django.shortcuts import render
from .models import ProductCategory
from .models import SubCategory
from .models import Product

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


def main(request):
    return render(request, 'mainapp/index.html', ({'title': name_main,
                                                   'links_main_menu': links_main_menu
                                                   }))


def categories(request):
    categories_list = ProductCategory.objects.all()
    return render(request, 'mainapp/categories.html', ({'title': name_categories,
                                                        'links_main_menu': links_main_menu,
                                                        'items_list': categories_list,
                                                        'menu_categories_list': categories_list,
                                                        'type': 'categories',
                                                        }))


def subCategories(request, cat_id):
    categories_list = ProductCategory.objects.all()
    subcategories_list = SubCategory.objects.filter(category=cat_id)
    return render(request, 'mainapp/categories.html', ({'title': name_categories,
                                                        'links_main_menu': links_main_menu,
                                                        'items_list': subcategories_list,
                                                        'menu_categories_list': categories_list,
                                                        'menu_subcategories_list': subcategories_list,
                                                        'cat_id': int(cat_id),
                                                        'type': 'subCategories',
                                                        }))


def productsOfCategory(request, cat_id, subcat_id):
    categories_list = ProductCategory.objects.all()
    subcategories_list = SubCategory.objects.filter(category=cat_id)
    products_list = Product.objects.filter(subcategory=subcat_id)
    return render(request, 'mainapp/categories.html', ({'title': name_categories,
                                                        'links_main_menu': links_main_menu,
                                                        'items_list': products_list,
                                                        'menu_categories_list': categories_list,
                                                        'menu_subcategories_list': subcategories_list,
                                                        'cat_id': int(cat_id),
                                                        'subcat_id': int(subcat_id),
                                                        'type': 'productsOfCategory',
                                                        }))


def products(request, cat_id, subcat_id, product_id):
    categories_list = ProductCategory.objects.all()
    subcategories_list = SubCategory.objects.filter(category=cat_id)
    product_item = Product.objects.get(pk=product_id)
    return render(request, 'mainapp/products.html', ({'title': name_products,
                                                      'links_main_menu': links_main_menu,
                                                      'product': product_item,
                                                      'menu_categories_list': categories_list,
                                                      'menu_subcategories_list': subcategories_list,
                                                      'cat_id': int(cat_id),
                                                      'subcat_id': int(subcat_id),
                                                      'type': 'products',
                                                      }))


def contacts(request):
    return render(request, 'mainapp/contacts.html', ({'title': name_contacts,
                                                      'links_main_menu': links_main_menu
                                                      }))
