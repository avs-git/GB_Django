def basket(request):
    basket = []
    if request.user.is_authenticated:
        basket = request.user.basket.all().order_by('product__category')
    return {
        'basket': basket,
    }


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


def links_main_menu():
    content = {
        'links_main_menu': links_main_menu,
    }
    return content
