from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from mainapp.models import Product
from ordersapp.forms import OrderItemForm
from ordersapp.models import Order, OrderItem
from .signals import *


class OrderListView(ListView):
    model = Order
    template_name = 'ordersapp/order_list.html'

    def get_queryset(self):
        return super(OrderListView, self).get_queryset().filter(is_active=True, user=self.request.user)


class OrderCreateView(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        if self.request.method == 'POST':
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if basket_items.exists():
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=basket_items.count())
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].price
            else:
                formset = OrderFormSet()

        context_data['orderitems'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        orderitems = context_data['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
            basket_items = Basket.objects.filter(user=self.request.user)
            basket_items.delete()

        if self.object.get_total_quantity == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderReadView(DetailView):
    model = Order
    template_name = 'ordersapp/order_detail.html'


class OrderUpdateView(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:list')
    template_name = 'ordersapp/order_form.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        if self.request.method == 'POST':
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object, queryset=self.object.orderitems.select_related())
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price

        context_data['orderitems'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        orderitems = context_data['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_quantity == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:list')


def complete(request, pk):
    order_item = Order.objects.get(pk=pk)
    order_item.status = Order.STATUS_SENT_TO_PROCEED
    order_item.save()
    return HttpResponseRedirect(reverse('ordersapp:list'))


def get_product_price(request, pk):
    product_price = 0
    product = Product.objects.filter(pk=pk, is_active=True).first()
    if product:
        product_price = product.price
    return JsonResponse(data={'price': product_price})
