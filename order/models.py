from django.contrib.postgres.fields import ArrayField
from django.db import models
import uuid


class ActiveOrderManager(models.Manager):
    def get_queryset(self):
        return super(ActiveOrderManager, self).get_queryset().filter(is_order_cancelled=False)


class CancelledOrderManager(models.Manager):
    def get_queryset(self):
        return super(CancelledOrderManager, self).get_queryset().filter(is_order_cancelled=True)


class ActiveOrderItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_item_cancelled=False)


class CancelledOrderItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_item_cancelled=True)


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Order(TimeStampedModel):
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Complete', 'Complete'),
        ('Failed', 'Failed'),
    ]

    STATUS = (
        ("Placed", "Placed"),
        ("Confirmed", "Confirmed"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=50)
    delivery_address_id = models.CharField(max_length=50)
    order_delivery_status = models.CharField(max_length=15, choices=STATUS, default="Placed")
    order_payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default="Pending")
    delivery_charge = models.FloatField(null=True, blank=True, default=0.0)
    order_total_price = models.FloatField(null=True, blank=True, default=0.0)
    is_order_cancelled = models.BooleanField(default=False)

    objects = models.Manager()
    active_orders = ActiveOrderManager()
    cancelled_orders = CancelledOrderManager()

    class Meta:
        db_table = "orders"
        ordering = ['-created_at']


class OrderItem(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    variation_ids = ArrayField(models.CharField(max_length=36), null=True)
    product_id = models.CharField(max_length=50)
    item_price = models.FloatField(default=0.0)
    quantity = models.IntegerField()
    is_item_cancelled = models.BooleanField(default=False)

    objects = models.Manager()
    active_order_items = ActiveOrderItemManager()
    cancelled_order_items = CancelledOrderItemManager()

    class Meta:
        db_table = 'order_items'
        ordering = ['item_price']


class OrderCancellation(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="order_cancels")
    order_cancel_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.order_cancel_reason[:20]


class OrderItemCancellation(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_item = models.OneToOneField(OrderItem, on_delete=models.CASCADE, related_name="order_item_cancels")
    order_item_cancel_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.order_item_cancel_reason[:20]
