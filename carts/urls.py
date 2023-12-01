from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name="cart"),
    path('add_cart/<int:product_id>/', views.addCart, name="add_cart"),
    path('remove_cart/<int:product_id>/', views.removeCart, name="remove_cart"),
    path('remove_full_item/<int:product_id>/', views.removeFullCartItem, name="remove_full_item"),
    path('checkout/', views.checkout, name="checkout"),
]