import json
import random

from django.conf import settings
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import ProductCategory, Product

POPULAR_SIZE = 4
SAME_PRODUCTS_SIZE = 3


def get_hot_product():
    return random.sample(list(Product.objects.all()), 1)[0]


def get_same_products(hot_product: Product):
    same_products_list = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)
    return same_products_list[:SAME_PRODUCTS_SIZE]


def index(request):
    popular_products = random.sample(list(Product.objects.all()), POPULAR_SIZE)
    basket = Basket.get_total_price_and_quantity(request.user)
    return render(request, 'mainapp/index.html', {'products': popular_products, 'basket': basket})


def products(request, pk=None, page=1):
    links_menu = ProductCategory.objects.all()[:4]
    if pk is not None:
        if pk == 0:
            category_item = {'name': 'Все', 'pk': '0'}
            products_list = Product.objects.all()
        else:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk)

        paginator = Paginator(products_list, 2)
        if not 1 <= page <= paginator.num_pages:
            raise Http404()
        products_paginator = paginator.page(page)

        context = {
            'links_menu': links_menu,
            'products': products_paginator,
            'category': category_item,
            'basket': Basket.get_total_price_and_quantity(request.user)
        }
        return render(request, 'mainapp/products_list.html', context)
    hot_product = get_hot_product()
    context = {
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': get_same_products(hot_product),
        'basket': Basket.get_total_price_and_quantity(request.user)
    }
    return render(request, 'mainapp/products.html', context)


def contact(request):
    with open(f'{settings.BASE_DIR}/json/contacts.json', encoding='utf-8') as input_file:
        contacts = json.load(input_file)
    return render(request, 'mainapp/contact.html', {'contacts': contacts})


def product(request, pk):
    context = {
        'links_menu': random.sample(list(ProductCategory.objects.all()), 4),
        'product': get_object_or_404(Product, pk=pk),
        'basket': Basket.get_total_price_and_quantity(request.user)
    }
    return render(request, 'mainapp/product.html', context)
