from django.conf import settings
from django.db import models

from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_total_price_and_quantity(cls, user: settings.AUTH_USER_MODEL):
        if not user.is_authenticated:
            return {'total_count': 0, 'total_price': 0}
        result_quantity = 0
        result_price = 0
        user_baskets = cls.objects.filter(user=user)
        for basket in user_baskets:
            result_quantity += basket.quantity
            result_price += basket.quantity * basket.product.price
        return {'total_count': result_quantity, 'total_price': result_price}

    @property
    def product_cost(self):
        return self.quantity * self.product.price
