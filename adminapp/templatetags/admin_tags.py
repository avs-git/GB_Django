from django import template
from mainapp.models import Product

register = template.Library()


@register.filter(name='products_count')
def products_count(category):
    quantity = len(Product.objects.filter(category=category.pk))
    return quantity
