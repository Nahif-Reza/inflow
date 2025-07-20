from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'sku', 'cost_price', 'sell_price', 'stock_quantity']


class RestockForm(forms.Form):
    SUPPLIER_CHOICES = [
        ('Supplier A', 'Supplier A'),
        ('Supplier B', 'Supplier B'),
        ('Supplier C', 'Supplier C'),
        ('Supplier D', 'Supplier D'),
        ('Supplier E', 'Supplier E'),
        ('Supplier F', 'Supplier F'),
    ]
    supplier = forms.ChoiceField(choices=SUPPLIER_CHOICES, label="Select Supplier")
    quantity = forms.IntegerField(min_value=1, label="Quantity to Add")

