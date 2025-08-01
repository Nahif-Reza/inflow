from django.db.models import Q, Sum, F
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from .forms import ProductForm, RestockForm, CategoryForm
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def product_list(request):
    query = request.GET.get('q')  # 'q' will come from the search form
    context = {}
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(id__icontains=query)
        )
    else:
        products = Product.objects.all()
        categories = Category.objects.all()
        total_products = products.count()
        total_categories = categories.count()
        total_stock_value = products.aggregate(
            total_value=Sum(F('cost_price') * F('stock_quantity'))
        )['total_value'] or 0
        low_stock_count = products.filter(stock_quantity__lt=5).count()
        context = {
            'products': products,
            'categories': categories,
            'total_products': total_products,
            'total_categories': total_categories,
            'total_stock_value': total_stock_value,
            'low_stock_count': low_stock_count,
        }
    return render(request, 'inventory/product_list.html', context)

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
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = CategoryForm()
    return render(request, 'inventory/add_category.html', {'form': form})

@staff_member_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
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

@staff_member_required
def view_categories(request):
    categories = Category.objects.all()
    return render(request, 'inventory/view_categories.html', {'categories': categories})

@staff_member_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('view_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'inventory/edit_category.html', {'form': form, 'category': category})

@staff_member_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('view_categories')


