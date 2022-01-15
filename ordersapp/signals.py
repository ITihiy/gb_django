from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from basketapp.models import Basket
from ordersapp.models import OrderItem


@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_on_save(sender, instance, **kwargs):
    if instance.pk:
        instance.product.quantity -= instance.quantity - sender.get_item(instance.pk).quantity

    else:
        instance.product.quantity -= instance.quantity

    instance.product.quantity = instance.product.quantity if instance.product.quantity >= 0 else 0
    instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_on_delete(sender, instance, **kwargs  ):
    instance.product.quantity += instance.quantity
    instance.product.save()
