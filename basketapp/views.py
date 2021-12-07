from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from basketapp.models import Basket
from mainapp.models import Product


@login_required
def basket(request):
    basket_totals = Basket.get_total_price_and_quantity(request.user)
    context = {
        'basket_list': Basket.objects.filter(user=request.user),
        'basket_totals': basket_totals,
    }
    return render(request, 'basketapp/basket.html', context)


@login_required
def basket_add(request, pk):
    if 'login' in request.META['HTTP_REFERER']:
        return HttpResponseRedirect(reverse('products:product', args=[pk]))
    product_item = get_object_or_404(Product, pk=pk)
    basket_item = Basket.objects.filter(user=request.user, product=product_item).first()
    if not basket_item:
        basket_item = Basket(user=request.user, product=product_item)
    basket_item.quantity += 1
    basket_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    basket_item = get_object_or_404(Basket, pk=pk)
    basket_item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        basket_item = Basket.objects.get(pk=pk)
        if basket_item.quantity > 0:
            basket_item.quantity = quantity
            basket_item.save()
        else:
            basket_item.delete()
        context = {
            'basket_list': Basket.objects.filter(user=request.user),
            'basket_totals': Basket.get_total_price_and_quantity(request.user),
        }
        result = render_to_string('basketapp/includes/inc_basket_list.html', context)
        return JsonResponse({'result': result})
