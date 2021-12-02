import json
import random

from django.conf import settings
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import ProductCategory, Product

POPULAR_SIZE = 4


def index(request):
    popular_products = random.sample(list(Product.objects.all()), POPULAR_SIZE)
    basket = Basket.get_total_price_and_quantity(request.user) if request.user.is_authenticated else {'total_count': 0,
                                                                                                      'total_price': 0.0}
    return render(request, 'mainapp/index.html', {'products': popular_products, 'basket': basket})


def products(request, pk=None):
    links_menu = ProductCategory.objects.all()[:4]
    if pk is not None:
        if pk == 0:
            category_item = {'name': 'Все', 'pk': '0'}
            products_list = Product.objects.all()
        else:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk)

        context = {
            'links_menu': links_menu,
            'products': products_list,
            'category': category_item,
            'basket': Basket.get_total_price_and_quantity(request.user) if request.user.is_authenticated
            else {'total_count': 0, 'total_price': 0.0}
        }
        return render(request, 'mainapp/products_list.html', context)
    context = {
        'links_menu': links_menu,
        'hot_product': Product.objects.first(),
        'same_products': Product.objects.all()[10:14],
        'basket': Basket.get_total_price_and_quantity(request.user) if request.user.is_authenticated
        else {'total_count': 0, 'total_price': 0.0}
    }
    return render(request, 'mainapp/products.html', context)


def contact(request):
    with open(f'{settings.BASE_DIR}/json/contacts.json', encoding='utf-8') as input_file:
        contacts = json.load(input_file)
    return render(request, 'mainapp/contact.html', {'contacts': contacts})
