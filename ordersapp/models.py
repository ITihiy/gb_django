from django.conf import settings
from django.db import models

from mainapp.models import Product


class Order(models.Model):
    STATUS_FORMING = 'FM'
    STATUS_SENT_TO_PROCEED = 'STP'
    STATUS_PROCEEDED = 'PRD'
    STATUS_PAID = 'PD'
    STATUS_CANCEL = 'CNL'
    STATUS_DONE = 'DN'

    STATUSES = (
        ((STATUS_FORMING), 'forming'),
         (STATUS_SENT_TO_PROCEED, 'sent to proceed'),
         (STATUS_PROCEEDED, 'proceeded'),
         (STATUS_PAID, 'paid'),
         (STATUS_CANCEL,'canceled'),
         (STATUS_DONE, 'done'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUSES, default=STATUS_FORMING, max_length=3)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_quantity(self):
        return sum(item.quantity for item in self.order_items.select_related())

    def get_total_cost(self):
        return sum(item.get_product_cost() for item in self.order_items.select_related())

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ', related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')

    def get_product_cost(self):
        return self.product.price * self.quantity
