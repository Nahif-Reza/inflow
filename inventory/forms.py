from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'sku', 'cost_price', 'sell_price', 'stock_quantity', 'category', 'image']

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

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-700 rounded-lg bg-gray-800 text-white',
                'placeholder': 'Category Name',
                'autofocus': True,
            }),
        }

    # Optional: make image field clearable with checkbox
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={
        'class': 'w-full text-white'
    }))