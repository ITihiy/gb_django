from django import template
from django.conf import settings


register = template.Library()


@register.filter(name='media_for_users')
def media_for_users(avatar):
    if not avatar:
        avatar = 'users/d29bebf9-ccb2-4489-8cb3-22691fa59a56.jpg'
    return f'{settings.MEDIA_URL}{avatar}'


@register.filter(name='media_for_products')
def media_for_products(image):
    if not image:
        image = 'products/istockphoto-1159568874-612x612.jpg'
    return f'{settings.MEDIA_URL}{image}'
