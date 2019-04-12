from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from basketapp.models import Basket
from django.urls import reverse
from mainapp.models import Product
from authapp.forms import ShopUserLoginForm
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse

# импортируем главное меню и корзину для отображения на всех страницах
from mainapp.views import common_content


@login_required
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


@login_required
def basket_add(request, pk):

    product = get_object_or_404(Product, pk=pk)

    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()
    if request.is_ajax():
        content = {
            'totalCost': basket.total_cost
        }
        return JsonResponse(content)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
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


@login_required
def basket_remove_item(request, pk):
    product = get_object_or_404(Product, pk=pk)
    basket = Basket.objects.filter(user=request.user, product=product).first()
    basket.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_drop(request):
    basket = Basket.objects.filter(user=request.user)
    basket.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user)

        content = {
            'basket_items': basket_items,
        }

        result = render_to_string('basketapp/includes/inc_basket_list.html', content)

        return JsonResponse({'result': result})
