import json

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from mainapp.models import ProductCategory, Product


def index(request):
    return render(request, 'mainapp/index.html')


def products(request, pk=None):
    links_menu = ProductCategory.objects.all()[:4]
    return render(request, 'mainapp/products.html', {'links_menu': links_menu})


def contact(request):
    with open('contacts.json') as input_file:
        contacts = json.load(input_file)
    return render(request, 'mainapp/contact.html', {'contacts': contacts})


def flush_and_populate(request):
    if settings.DEBUG:
        Product.objects.all().delete()
        ProductCategory.objects.all().delete()
        with open(settings.BASE_DIR / 'products.json', encoding='utf-8') as file_in:
            json_data = json.load(file_in)
            for current_product in json_data:
                current_cat_name = current_product['category']['name']
                current_cat_desc = current_product['category']['description']
                category, created = ProductCategory.objects.get_or_create(name=current_cat_name,
                                                                          description=current_cat_desc)

                product = Product.objects.create(category=category, name=current_product['name'],
                                                 short_description=current_product['short_description'],
                                                 description=current_product['description'])
                product.save()
        return HttpResponse('finished')
    else:
        return HttpResponse('Get out of here, you bastard')
