import json

from django.shortcuts import render


def index(request):
    return render(request, 'mainapp/index.html')


links_menu = [
    {'category_link': 'home', 'category_name': 'дом'},
    {'category_link': 'office', 'category_name': 'офис'},
    {'category_link': 'modern', 'category_name': 'модерн'},
    {'category_link': 'classic', 'category_name': 'классика'},
]


def products(request, category=None):
    return render(request, 'mainapp/products.html', {'links_menu': links_menu})


def contact(request):
    with open('contacts.json') as input_file:
        contacts = json.load(input_file)
    return render(request, 'mainapp/contact.html', {'contacts': contacts})
