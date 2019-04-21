from django import template


register = template.Library()


@register.filter(name='basket_total_cost')
def basket_total_cost(user):
    if user.is_anonymous:
        return 0
    else:
        items = user.basket.select_related('product').all()
        # items = Basket.objects.filter(user=user)
        totalcost = sum(list(map(lambda x: x.product.price*x.quantity, items)))
        return totalcost
