from authapp.models import ShopUser
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, render
from django.forms import inlineformset_factory
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from adminapp.forms import CategoryEditForm
from django.db import transaction

from mainapp.views import get_strucured_categories
from mainapp.models import Product, Category

from ordersapp.models import Order, OrderItem
from ordersapp.forms import OrderItemForm, OrderForm


class IsSuperUserView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class CategoryListView(IsSuperUserView, ListView):
    model = Category
    template_name = 'adminapp/categories.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['title'] = 'Список категорий'
        return context

    # переопределяем эту функцию для вывода категорий согласно вложенности
    def get_queryset(self):
        return get_strucured_categories()


class CategoryCreateView(IsSuperUserView, CreateView):
    form_class = CategoryEditForm
    # model = Category
    template_name = 'adminapp/categories_update.html'
    # fields = '__all__'
    exclude = 'nesting_level'
    success_url = reverse_lazy('myadmin:categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание категории'
        return context


class CategoryUpdateView(IsSuperUserView, UpdateView):
    form_class = CategoryEditForm
    template_name = 'adminapp/categories_update.html'
    exclude = 'nesting_level'
    success_url = reverse_lazy('myadmin:categories')
    model = Category

    def get_context_data(self, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Изменение категории'
        return context


class CategoryDeleteView(IsSuperUserView, DeleteView):
    model = Category
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('myadmin:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        is_delete = request.POST.get('delete')

        if is_delete:
            self.object.delete()
        else:
            self.object.is_active = False
            self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ShopUserListView(IsSuperUserView, ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    def get_context_data(self, **kwargs):
        context = super(ShopUserListView, self).get_context_data(**kwargs)
        context['title'] = 'Список пользователей'
        return context

    def get_queryset(self):
        queryset = ShopUser.objects.all().order_by('-is_active')
        return queryset


class ShopUserCreateView(IsSuperUserView, CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    fields = '__all__'
    success_url = reverse_lazy('myadmin:users')

    def get_context_data(self, **kwargs):
        context = super(ShopUserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Создание пользователя'
        return context


class ShopUserUpdateView(IsSuperUserView, UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    fields = '__all__'
    success_url = reverse_lazy('myadmin:users')

    def get_context_data(self, **kwargs):
        context = super(ShopUserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Изменение пользователя'
        return context


class ShopUserDeleteView(IsSuperUserView, DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('myadmin:users')

    def get_context_data(self, **kwargs):
        print(self.kwargs)
        context = super(ShopUserDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Удаление пользователя'
        context['user_to_delete'] = get_object_or_404(ShopUser, pk=self.kwargs['pk'])
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        is_delete = request.POST.get('delete')

        if is_delete:
            self.object.delete()
        else:
            self.object.is_active = False
            self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ProductListView(IsSuperUserView, ListView):
    model = Product
    template_name = 'adminapp/products.html'

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['title'] = 'Список товаров'
        return context

    def get_queryset(self):
        queryset = Product.objects.filter(category=self.kwargs['pk'])
        return queryset


class ProductCreateView(IsSuperUserView, CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        self.success_url = reverse_lazy('myadmin:products', kwargs={'pk': self.kwargs['pk']})
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Создание товара'
        return context

    def get_initial(self):
        self.initial['category'] = self.kwargs['pk']
        return self.initial

    def get_success_url(self):
        return reverse_lazy('myadmin:products', kwargs=self.kwargs)


class ProductUpdateView(IsSuperUserView, UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Изменение товара'
        return context

    def get_success_url(self):
        category_pk = get_object_or_404(Product, pk=self.kwargs['pk']).category.pk
        return reverse_lazy('myadmin:products', kwargs={'pk': category_pk})


class ProductDeleteView(IsSuperUserView, DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    def get_context_data(self, **kwargs):
        category_pk = get_object_or_404(Product, pk=self.kwargs['pk']).category.pk
        product_to_delete = get_object_or_404(Product, pk=self.kwargs['pk'])

        context = super(ProductDeleteView, self).get_context_data(**kwargs)
        context['category_pk'] = category_pk
        context['product_to_delete'] = product_to_delete
        context['title'] = 'удаление товара'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        is_delete = request.POST.get('delete')

        if is_delete:
            self.object.delete()
        else:
            self.object.is_active = False
            self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('myadmin:categories')


class OrderListView(IsSuperUserView, ListView):
    model = Order
    template_name = 'adminapp/orders.html'

    def get_queryset(self):
        return Order.objects.all()


class OrderUpdateView(IsSuperUserView, UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('myadmin:orders')
    template_name = 'adminapp/order_update.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order,
                                             OrderItem,
                                             form=OrderForm,
                                             can_order=True,
                                             extra=0,
                                             )
        if self.request.POST:
            data['orderitems'] = OrderFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['orderitems'] = OrderFormSet(instance=self.object)
            data['order_status_choices'] = Order.ORDER_STATUS_CHOICES

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderDeleteView(IsSuperUserView, DeleteView):
    model = Order
    success_url = reverse_lazy('myadmin:orders')
    template_name = 'adminapp/order_confirm_delete.html'


def order_change_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    new_status = request.POST.get('order_status_choice')
    print(new_status)
    order.status = new_status
    order.save()

    return HttpResponseRedirect(reverse_lazy('myadmin:orders'))
