from django.urls import path

from . import views

urlpatterns = [
    path("", views.get_product_list, name="product_list"),
    path("add-to-cart/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.get_cart_items, name="shopping_cart"),
    path("stripe-config/", views.get_stripe_config, name="stripe_config"),
    path("checkout/", views.create_checkout_session),
    path("success/", views.payment_success),
    path("cancel/", views.payment_cancel),
]
