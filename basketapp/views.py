from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from basketapp.models import Basket
from mainapp.models import Product

# импортируем главное меню и корзину для отображения на всех страницах
from mainapp.views import common_content


def basket(request):
    basket = []
    basket = Basket.objects.filter(user=request.user)
    basket.sum = 0
    for item in basket:
        item.sum = item.product.price * item.quantity
        basket.sum += item.sum
    content = {
        **common_content(request),
        'basket': basket
    }

    return render(request, 'basketapp/basket.html', content)


def basket_add(request, pk):
    product = get_object_or_404(Product, pk=pk)

    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_remove(request, pk):
    product = get_object_or_404(Product, pk=pk)
    basket = Basket.objects.filter(user=request.user, product=product).first()
    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity -= 1
    if basket.quantity == 0:
        basket.delete()
    else:
        basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_remove_item(request, pk):
    product = get_object_or_404(Product, pk=pk)
    basket = Basket.objects.filter(user=request.user, product=product).first()
    basket.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_drop(request):
    basket = Basket.objects.filter(user=request.user)
    basket.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
