from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)


    def __str__(self):
        return self.name

class StorageLocation(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=10, unique=True)
    category = models.ForeignKey(Category, blank=True, on_delete=models.SET_NULL, null = True)
    location = models.ForeignKey(StorageLocation, blank=True, on_delete=models.SET_NULL, null = True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=10)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    @property
    def is_stock_low(self):
        return self.stock_quantity < self.low_stock_threshold

    def __str__(self):
        return self.name