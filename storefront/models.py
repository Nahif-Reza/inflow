from itertools import product

from django.db import models
from inventory.models import Product
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11, unique=True)
    address = models.TextField()

    def __str__(self):
        return self.user.username

class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_subtotal(self):
        subtotal = 0
        for item in self.cart_items.all():
            subtotal += item.product.sell_price * item.quantity
        return subtotal

    def __str__(self):
        return f"Cart of {self.customer.user.first_name}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    @property
    def total_price(self):
        return self.product.sell_price * self.quantity


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    placed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled")
    ], default="pending")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_option = models.CharField(max_length=20, choices=[
        ("pickup", "Pickup"),
        ("home_delivery", "Home Delivery")
    ])

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_subtotal(self):
        return self.unit_price * self.quantity