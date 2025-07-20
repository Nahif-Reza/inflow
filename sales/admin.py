from django.contrib import admin
from .models import Invoice
from .models import InvoiceItem
from .models import Transaction


admin.site.register(Invoice)
admin.site.register(InvoiceItem)
admin.site.register(Transaction)

