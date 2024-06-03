from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add-to-cart/<slug>', views.add_to_cart, name="add_to_cart"),
    path('remove-cart-item/<int:product_id>/<int:cart_item_id>/',
         views.remove_cart_item, name='remove_cart_item'),
    path('increment-cart-item/<int:product_id>/<int:cart_item_id>/',
         views.increment_cart_item, name='increment_cart_item'),
    path('decrement-cart-item/<int:product_id>/<int:cart_item_id>/',
         views.decrement_cart_item, name='decrement_cart_item'),
    path('checkout/', views.checkout, name="checkout"),
]
