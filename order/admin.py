from django.contrib import admin
from .models import Order, OrderItem


class OrdersModel(admin.ModelAdmin):
    list_display = (
        'order_delivery_status', 'user_id', 'delivery_address_id', 'delivery_charge', 'order_payment_status', 'is_order_cancelled', 'created_at')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('delivery_address_id',)


class OrderItemsModel(admin.ModelAdmin):
    list_display = ('id', 'order', 'product_id', 'item_price', 'quantity', 'is_item_cancelled', 'modified_at')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('item_price',)


class OrderCancellationModel(admin.ModelAdmin):
    list_display = ('id', 'order_cancel_reason')


admin.site.register(Order, OrdersModel)
admin.site.register(OrderItem, OrderItemsModel)
