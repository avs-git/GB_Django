from authapp.models import ShopUser
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, render
from mainapp.models import Product, Category
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from authapp.forms import ShopUserRegisterForm
from adminapp.forms import ShopUserAdminEditForm, CategoryEditForm, ProductEditForm
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator


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


class CategoryCreateView(IsSuperUserView, CreateView):
    model = Category
    template_name = 'adminapp/categories_update.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:categories')

    def get_context_data(self, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Создание категории'
        return context


class CategoryUpdateView(IsSuperUserView, UpdateView):
    model = Category
    template_name = 'adminapp/categories_update.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:categories')

    def get_context_data(self, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Изменение категории'
        return context


class CategoryDeleteView(IsSuperUserView, DeleteView):
    model = Category
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
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


class ShopUserCreateView(IsSuperUserView, CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:users')

    def get_context_data(self, **kwargs):
        context = super(ShopUserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Создание пользователя'
        return context


class ShopUserUpdateView(IsSuperUserView, UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:users')

    def get_context_data(self, **kwargs):
        context = super(ShopUserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Изменение пользователя'
        return context


class ShopUserDeleteView(IsSuperUserView, DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin:users')

    def get_context_data(self, **kwargs):
        context = super(ShopUserDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Удаление пользователя'
        return context

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(ShopUser, pk=kwargs['pk'])
        user.is_active = False
        user.save()
        return HttpResponseRedirect(self.success_url)


class ProductListView(IsSuperUserView, ListView):
    model = Product
    template_name = 'adminapp/products.html'

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['object_list'] = Product.objects.filter(category=self.kwargs['pk'])
        context['title'] = 'Список товаров'
        return context


class ProductCreateView(IsSuperUserView, CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        self.success_url = reverse_lazy('admin:products', kwargs={'pk': self.kwargs['pk']})
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Создание товара'
        return context

    def get_initial(self):
        self.initial['category'] = self.kwargs['pk']
        return self.initial

    def get_success_url(self):
        return reverse_lazy('admin:products', kwargs=self.kwargs)


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
        return reverse_lazy('admin:products', kwargs={'pk': category_pk})


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
        product = get_object_or_404(Product, pk=kwargs['pk'])
        product.is_active = False
        product.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        category_pk = get_object_or_404(Product, pk=self.kwargs['pk']).category.pk
        return reverse_lazy('admin:products', kwargs={'pk': category_pk})

# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     title = 'админка/пользователи'
#
#     users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#
#     content = {
#         'title': title,
#         'objects': users_list
#     }
#
#     return render(request, 'adminapp/users.html', content)
#
#
# @user_passes_test(lambda u: u.is_superuser)
# def user_create(request):
#     title = 'пользователи/создание'
#
#     if request.method == 'POST':
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin:users'))
#     else:
#         user_form = ShopUserRegisterForm()
#
#     content = {'title': title, 'update_form': user_form}
#
#     return render(request, 'adminapp/user_update.html', content)
#
#
# @user_passes_test(lambda u: u.is_superuser)
# def user_update(request, pk):
#     title = 'пользователи/редактирование'
#
#     edit_user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('admin:user_update', args=[edit_user.pk]))
#     else:
#         edit_form = ShopUserAdminEditForm(instance=edit_user)
#
#     content = {'title': title, 'update_form': edit_form}
#
#     return render(request, 'adminapp/user_update.html', content)
#
#
# @user_passes_test(lambda u: u.is_superuser)
# def user_delete(request, pk):
#     title = 'пользователи/удаление'
#
#     user = get_object_or_404(ShopUser, pk=pk)
#
#     if request.method == 'POST':
#         user.is_active = False
#         user.save()
#         return HttpResponseRedirect(reverse('admin:users'))
#
#     content = {'title': title, 'user_to_delete': user}
#
#     return render(request, 'adminapp/user_delete.html', content)
#
#
# @user_passes_test(lambda u: u.is_superuser)
# def categories(request):
#     title = 'админка/категории'
#
#     categories_list = Category.objects.all()
#
#     content = {
#         'title': title,
#         'objects': categories_list
#     }
#
#     return render(request, 'adminapp/categories.html', content)
#
#
# @user_passes_test(lambda u: u.is_superuser)
# def category_create(request):
#     title = 'категории/создание'
#
#     if request.method == 'POST':
#         category_form = CategoryEditForm(request.POST, request.FILES)
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('admin:categories'))
#     else:
#         category_form = CategoryEditForm()
#
#     content = {'title': title, 'update_form': category_form}
#
#     return render(request, 'adminapp/categories_update.html', content)
#
#
# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):
#     title = 'категория/редактирование'
#
#     edit_category = get_object_or_404(Category, pk=pk)
#     if request.method == 'POST':
#         edit_form = CategoryEditForm(request.POST, request.FILES, instance=edit_category)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('admin:category_update', args=[edit_category.pk]))
#     else:
#         edit_form = CategoryEditForm(instance=edit_category)
#
#     content = {'title': title, 'update_form': edit_form}
#
#     return render(request, 'adminapp/categories_update.html', content)
#
#
# @user_passes_test(lambda u: u.is_superuser)
# def category_delete(request, pk):
#     title = 'категории/удаление'
#
#     category = get_object_or_404(Category, pk=pk)
#
#     if request.method == 'POST':
#         category.is_active = False
#         category.save()
#         return HttpResponseRedirect(reverse('admin:categories'))
#
#     content = {'title': title, 'category_to_delete': category}
#
#     return render(request, 'adminapp/category_delete.html', content)
#
#
# @user_passes_test(lambda u: u.is_superuser)
# def products(request, pk):
#     title = 'админка/продукт'
#
#     category = get_object_or_404(Category, pk=pk)
#     products_list = Product.objects.filter(category__pk=pk).order_by('name')
#
#     content = {
#         'title': title,
#         'category': category,
#         'objects': products_list,
#     }
#
#     return render(request, 'adminapp/products.html', content)
#
#
# @user_passes_test(lambda u: u.is_superuser)
# def product_read(request, pk):
#     title = 'продукт/подробнее'
#     product = get_object_or_404(Product, pk=pk)
#     content = {'title': title, 'object': product, }
#
#     return render(request, 'adminapp/product_read.html', content)
#
#
# def product_create(request, pk):
#     title = 'продукт/создание'
#     category = get_object_or_404(Category, pk=pk)
#
#     if request.method == 'POST':
#         product_form = ProductEditForm(request.POST, request.FILES)
#         if product_form.is_valid():
#             product_form.save()
#             return HttpResponseRedirect(reverse('admin:products', args=[pk]))
#     else:
#         product_form = ProductEditForm(initial={'category': category})
#         content = {'title': title,
#                    'update_form': product_form,
#                    'category': category
#                    }
#
#         return render(request, 'adminapp/product_update.html', content)
#
#
# def product_update(request, pk):
#     title = 'продукт/редактирование'
#
#     edit_product = get_object_or_404(Product, pk=pk)
#
#     if request.method == 'POST':
#         edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('admin:product_update', args=[edit_product.pk]))
#     else:
#         edit_form = ProductEditForm(instance=edit_product)
#
#     content = {'title': title,
#                'update_form': edit_form,
#                'category': edit_product.category
#                }
#
#     return render(request, 'adminapp/product_update.html', content)
#
#
# def product_delete(request, pk):
#     title = 'продукт/удаление'
#
#     product = get_object_or_404(Product, pk=pk)
#
#     if request.method == 'POST':
#         product.is_active = False
#         product.save()
#         return HttpResponseRedirect(reverse('admin:products', args=[product.category.pk]))
#
#     content = {'title': title, 'product_to_delete': product}
#
#     return render(request, 'adminapp/product_delete.html', content)
