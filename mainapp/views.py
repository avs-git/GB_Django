from django.shortcuts import render, get_object_or_404
from .models import Category
from .models import Product
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

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


def get_strucured_categories(order='-is_active', is_active=0):
    if is_active:
        all_categories = Category.objects.all().filter(is_active=1)
    else:
        all_categories = Category.objects.all().order(order=order)

    structure = []

    def get_category_childs(_cat, _categories):
        childs = []

        for item in _categories:
            if item.parent == _cat:
                childs.append(item)

        return childs

    def get_parent_child_struct(cat):
        if not cat.parent and cat not in structure:
            structure.append(cat)

        for i in get_category_childs(cat, all_categories):
            if i not in structure:
                structure.append(i)

            get_parent_child_struct(i)

    for cat in all_categories:
        get_parent_child_struct(cat)

    return structure


def common_content(*args):
    content = {
        'links_main_menu': links_main_menu,
        'categories_menu': get_strucured_categories(is_active=1)
    }
    return content


def get_hot_product():
    _products = Product.objects.all().select_related()

    return random.sample(list(_products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk).select_related()[:3]

    return same_products


def main(request):
    content = {
        **common_content(),
        'title': name_main,
    }
    return render(request, 'mainapp/index.html', content)


class CategoriesList(ListView):
    model = Category
    template_name = 'mainapp/categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hot_product = get_hot_product()
        same_products = get_same_products(hot_product)
        categories_list = Category.objects.filter(nesting_level=0).filter(is_active=True)

        context['links_main_menu'] = links_main_menu
        context['categories_menu'] = get_strucured_categories(is_active=1)
        context['title'] = name_categories
        context['menu_categories_list'] = categories_list
        context['menu_subcategories_list'] = categories_list
        context['hot_product'] = hot_product
        context['same_products'] = same_products
        context['type'] = 'categories'

        return context


class ProductsList(ListView):
    model = Product
    template_name = 'mainapp/categories.html'
    paginate_by = 10
    allow_empty = True
    context_object_name = 'items_list'

    def get_queryset(self):
        cat_id = self.kwargs['cat_id']
        products_list = Product.objects.filter(category=cat_id, category__is_active=True, is_active=True)
        if len(products_list) == 0:
            if len(Category.objects.filter(parent=cat_id)) != 0:
                child_category = Category.objects.filter(parent=cat_id).select_related()
                for _category in child_category:
                    products_list = Product.objects.filter(category=_category.pk).select_related()
        return products_list

    def get_context_data(self, **kwargs):
        cat_id = self.kwargs['cat_id']
        hot_product = get_hot_product()
        same_products = get_same_products(hot_product)
        categories_list = Category.objects.filter(nesting_level=0, is_active=True)
        subcategories_list = Category.objects.filter(parent=cat_id, is_active=True)

        context = {
            **common_content(),
            'title': name_categories,
            'menu_categories_list': categories_list,
            'menu_subcategories_list': subcategories_list,
            'cat_id': int(cat_id),
            'hot_product': hot_product,
            'same_products': same_products,
            'type': 'productsOfCategory',
            **super().get_context_data(**kwargs),
        }

        return context


class ProductView(DetailView):
    model = Product
    template_name = 'mainapp/products.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        product_item = Product.objects.filter(pk=self.kwargs['pk']).select_related().first()
        categories_list = Category.objects.filter(nesting_level=0).filter(is_active=True).select_related()
        subcategories_list = Category.objects.filter(parent=product_item.category).filter(is_active=True).select_related()
        cat_id = product_item.category.id

        context = {
            **common_content(),
            'title': name_products,
            'menu_categories_list': categories_list,
            'menu_subcategories_list': subcategories_list,
            'cat_id': int(cat_id),
            'type': 'products',
            **super().get_context_data(**kwargs),
        }

        return context


def contacts(request):
    content = {
        **common_content(),
        'title': name_contacts,
    }
    return render(request, 'mainapp/contacts.html', content)
