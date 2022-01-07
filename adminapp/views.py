from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryForm, ProductForm, OrderUpdateStatusForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from ordersapp.models import Order


class AccessMixin:
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class OrdersListView(AccessMixin, ListView):
    model = Order
    template_name = 'adminapp/order_list.html'


class OrderStatusUpdateView(UpdateView):
    model = Order
    template_name = 'adminapp/order_form.html'
    form_class = OrderUpdateStatusForm
    success_url = reverse_lazy('adminapp:orders')


class UsersListView(AccessMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/users_list.html'


class UserCreateView(AccessMixin, CreateView):
    model = ShopUser
    form_class = ShopUserRegisterForm
    template_name = 'adminapp/user_form.html'
    success_url = reverse_lazy('adminapp:users')


class UserEditView(AccessMixin, UpdateView):
    model = ShopUser
    form_class = ShopUserAdminEditForm
    template_name = 'adminapp/user_form.html'
    success_url = reverse_lazy('adminapp:users')


class UserDeleteView(AccessMixin, DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('adminapp:users')


class ProductCategoryListView(AccessMixin, ListView):
    model = ProductCategory
    template_name = 'adminapp/categories_list.html'


class ProductCategoryCreateView(AccessMixin, CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_form.html'
    form_class = ProductCategoryForm
    success_url = reverse_lazy('adminapp:categories')


class ProductCategoryUpdateView(AccessMixin, UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_form.html'
    form_class = ProductCategoryForm
    success_url = reverse_lazy('adminapp:categories')


class ProductCategoryDelete(AccessMixin, DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_form.html'
    form_class = ProductCategoryForm
    success_url = reverse_lazy('adminapp:categories')


class ProductListView(AccessMixin, ListView):
    model = Product
    template_name = 'adminapp/product_list.html'

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Product.objects.filter(category__pk=pk)


class ProductCreateView(AccessMixin, CreateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('adminapp:categories')

    def _get_category(self):
        category_id = self.kwargs.get('pk')
        category_item = get_object_or_404(ProductCategory, pk=category_id)
        return category_item

    def get_success_url(self, **kwargs):
        return reverse('adminapp:products', args=[self._get_category().pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.request.method == 'GET':
            context_data['category'] = self._get_category()
        return context_data


class ProductEditView(AccessMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'adminapp/product_form.html'

    def _get_category(self):
        category_id = Product.objects.get(pk=self.kwargs.get('pk')).category_id
        category_item = get_object_or_404(ProductCategory, pk=category_id)
        return category_item

    def get_success_url(self, **kwargs):
        return reverse('adminapp:products', args=[self._get_category().pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.request.method == 'GET':
            context_data['category'] = self._get_category()
        return context_data


class ProductDeleteView(AccessMixin, DeleteView):
    model = Product
    form_class = ProductForm
    template_name = 'adminapp/product_delete.html'

    def _get_category(self):
        category_id = Product.objects.get(pk=self.kwargs.get('pk')).category_id
        category_item = get_object_or_404(ProductCategory, pk=category_id)
        return category_item

    def get_success_url(self, **kwargs):
        return reverse('adminapp:products', args=[self._get_category().pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['product_pk'] = self._get_category().pk
        return context_data


class ProductDetailView(AccessMixin, DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'
