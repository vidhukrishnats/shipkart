from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.placeOrder, name="place_order"),
    path('payments/', views.payments, name="payments"),
]
