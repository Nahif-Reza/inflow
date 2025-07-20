from django.shortcuts import render
from inventory.models import Product
from storefront.models import Order
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def manager_home(request):
    return render(request, 'dashboard/manager_home.html')

@staff_member_required
def all_orders(request):
    orders = Order.objects.select_related('customer__user').order_by('-placed_at')  # newest first
    return render(request, 'dashboard/all_orders.html', {'orders': orders})
