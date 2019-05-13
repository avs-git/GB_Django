from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='basket_total_cost')
def basket_total_cost(user):
    if user.is_anonymous:
        return 0
    else:
        items = user.basket.select_related('product').all()
        # items = Basket.objects.filter(user=user)
        totalcost = sum(list(map(lambda x: x.product.price * x.quantity, items)))
        return totalcost


@register.filter(name='mult')
def add_margin(value, mult):
    return int(value) * int(mult)


@register.filter(name='media_folder_products')
def media_folder_products(string):
    """
    Автоматически добавляет относительный URL-путь к медиафайлам продуктов
    products_images/product1.jpg --> /media/products_images/product1.jpg
    """
    if not string:
        string = 'products_images/default.jpg'

    return f'{settings.MEDIA_URL}{string}'
