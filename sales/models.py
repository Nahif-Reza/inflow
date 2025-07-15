from django.db import models
from inventory.models import Product


class Invoice(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits = 16, decimal_places=2)


    def __str__(self):
        return f"Invoice #{self.id} - {self.customer_name}"

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="item")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

class Transaction(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Transaction for Invoice #{self.invoice.id}"

# Ledger will be added here later