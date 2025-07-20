from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm, RestockForm
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def product_list(request):
    query = request.GET.get('q')  # 'q' will come from the search form
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(id__icontains=query)
        )
    else:
        products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})

@staff_member_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'inventory/add_product.html', {'form': form})

@staff_member_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)
    return render(request, "inventory/edit_product.html", {'form': form, 'product': product})


@staff_member_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('product_list')

@staff_member_required
def restock_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = RestockForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            supplier = form.cleaned_data['supplier']
            # Later will be used in ledger
            product.stock_quantity += quantity
            product.save()
            return redirect('product_list')
    else:
        form = RestockForm()
    return render(request, 'inventory/restock_product.html', {
        'form': form,
        'product': product
    })

