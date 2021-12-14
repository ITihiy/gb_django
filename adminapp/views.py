from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryForm, ProductForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


class AccessMixin:
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UsersListView(AccessMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/users_list.html'


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        user_form = ShopUserRegisterForm()
    return render(request, 'adminapp/user_form.html', {'form': user_form})


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    current_user = get_object_or_404(ShopUser, pk=pk, )
    if request.method == 'POST':
        user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        user_form = ShopUserAdminEditForm(instance=current_user)
    return render(request, 'adminapp/user_form.html', {'form': user_form})


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    current_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        current_user.is_active = False
        current_user.save()
        return HttpResponseRedirect(reverse('adminapp:users'))
    return render(request, 'adminapp/user_delete.html', {'object': current_user})


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    context = {
        'objects_list': ProductCategory.objects.all()
    }
    return render(request, 'adminapp/categories_list.html', context)


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


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    context = {
        'objects_list': Product.objects.filter(category__pk=pk)
    }
    return render(request, 'adminapp/products_list.html', context)


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


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    current_product = get_object_or_404(Product, pk=pk)
    current_category = ProductCategory.objects.get(pk=current_product.category_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=current_product)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:products', args=[current_category.pk]))
    else:
        form = ProductForm(instance=current_product)
    return render(request, 'adminapp/product_form.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    current_product = get_object_or_404(Product, pk=pk)
    current_category = ProductCategory.objects.get(pk=current_product.category_id)
    if request.method == 'POST':
        current_product.is_active = False
        current_product.save()
        return HttpResponseRedirect(reverse('adminapp:products', args=[current_category.pk]))
    return render(request, 'adminapp/product_delete.html', {'object': current_product, 'return_pk': current_category.pk})


class ProductDetailView(AccessMixin, DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'
