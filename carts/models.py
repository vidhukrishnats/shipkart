from django.db import models
from customer.models import Product, Category, CustomUser

class Cart(models.Model):
    cart_id = models.CharField(max_length=100, blank=True)
    date_added = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    def sub_total(self):
        return self.product.price * self.quantity
    def __str__(self):
        return f"{self.product.title} - Cart ID: {self.cart_id}"
