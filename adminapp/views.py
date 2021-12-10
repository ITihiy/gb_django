from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryForm, ProductForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    context = {
        'objects_list': ShopUser.objects.all().order_by('-is_active')
    }
    return render(request, 'adminapp/users_list.html', context)


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


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:categories'))
    else:
        form = ProductCategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'adminapp/category_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    current_category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST, instance=current_category)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:categories'))
    else:
        form = ProductCategoryForm(instance=current_category)
    return render(request, 'adminapp/category_form.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    current_category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        current_category.is_active = False
        current_category.save()
        return HttpResponseRedirect(reverse('adminapp:categories'))
    return render(request, 'adminapp/category_delete.html', {'object': current_category})


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    context = {
        'objects_list': Product.objects.filter(category__pk=pk)
    }
    return render(request, 'adminapp/products_list.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_product = Product.objects.create(**form.cleaned_data)
            new_product.save()
            return HttpResponseRedirect(reverse('adminapp:products', args=[new_product.category_id]))
    else:
        form = ProductForm()
    context = {
        'form': form,
    }
    return render(request, 'adminapp/product_form.html', context)


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


@user_passes_test(lambda u: u.is_superuser)
def product_read(request, pk):
    current_product = get_object_or_404(Product, pk=pk)
    return HttpResponseRedirect(reverse('products:product', args=[pk]))
