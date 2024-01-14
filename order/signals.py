from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order, OrderItem


@receiver(post_save, sender=OrderItem)
def post_save_order_total_price(sender, instance, created, **kwargs):
    if created:
        order_id = instance.order_id
        order = Order.objects.get(id=order_id)
        order.order_total_price += instance.item_price
        order.save()