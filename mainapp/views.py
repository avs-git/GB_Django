from django.shortcuts import render

# Названия страниц для title и названия в меню
name_main = 'Главная'
name_products = 'Товары'
name_contacts = 'Контакты'
name_vvs = 'vvs'

# Состав главного меню
links_main_menu = (
    {'href': 'index', 'name': name_main},
    {'href': 'products', 'name': name_products},
    {'href': 'contacts', 'name': name_contacts},
)

def main(request):
    return render(request, 'mainapp/index.html', ({'title': name_main, 'links_main_menu': links_main_menu}))


def products(request):
    return render(request, 'mainapp/products.html', ({'title': name_products, 'links_main_menu': links_main_menu}))


def contacts(request):
    return render(request, 'mainapp/contacts.html', ({'title': name_contacts, 'links_main_menu': links_main_menu}))
