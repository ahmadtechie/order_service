from django.urls import path
from rest_framework_nested import routers
from . import views

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

router = routers.DefaultRouter()
router.register('orders', views.OrderViewSet, basename='orders')

# TODO: Add endpoint that will enable an admin to update user order for tracking -done-
# TODO: Modify user order endpoints to only retrieve active orders
# TODO: Add endpoints to retrieve all orders irrespective of whether cancelled or not
# TODO: Add an endpoint that returns all cancelled orders

urlpatterns = [
    path('orders/user/<uuid:user_id>/', views.AllUserOrders.as_view(), name="order.history"),
    path('orders/<uuid:pk>/track', views.OrderTrackingUpdateView.as_view(), name="order.update"),
    path('orders/<uuid:order_id>/cancel/', views.OrderCancellationView.as_view(), name="order.cancel"),
    path('orders/<uuid:user_id>/mycancelled/', views.CancelledOrdersView.as_view(), name="order.cancel"),
    path('orders/<uuid:order_item_id>/orderitem/cancel/', views.OrderItemCancellationView.as_view(),
         name="order_item.cancel"),
    path('orders/<uuid:user_id>/orderitem/mycancelled/', views.CancelledOrderItemsView.as_view(),
         name="order_item.cancel.list"),
    path('orders/<uuid:user_id>/myactive/', views.UserActiveOrdersView.as_view(), name="order.cancel"),
    path('orders/<uuid:order_id>/orderitems/', views.OrderItemsView.as_view(), name="order.order_items.view"),
    path('orders/<uuid:order_id>/orderitems/create/', views.CreateOrderItemView.as_view(),
         name="order.order_items.create"),
    path('orders/<uuid:order_id>/orderitems/<uuid:order_item_id>/', views.RetrieveOrderItemView.as_view(),
         name="order.order_items.retrieve"),
    path('orders/cancelled/all/', views.CancelledOrdersView.as_view(), name="order.cancel"),
    path('orders/items-cancelled/all/', views.CancelledOrderItemsView.as_view(), name="order.cancel"),
    path('orders/api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('orders/api-docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

urlpatterns += router.urls
