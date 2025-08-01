from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from accounts.models import ManagerProfile
from .models import Customer, Order
from django.shortcuts import render, redirect, get_object_or_404
from inventory.models import Product, Category
from django.db.models import Q
from .models import Cart, CartItem
from .forms import ProfileForm, PasswordChangeForm


def storefront_home(request):
    query = request.GET.get('q')
    products = None
    categories = None
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query)
        )
    else:
        categories = Category.objects.all()
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        cart, created = Cart.objects.get_or_create(customer=customer)
        cart_items = cart.cart_items.all()
        cart_items_count = len(cart_items)
        cart_subtotal = cart.get_subtotal()
        context = {
            'categories': categories,
            'cart_items': cart_items,
            'cart_items_count': cart_items_count,
            'cart_subtotal': cart_subtotal
        }
    else:
        context = {
            'categories': categories
        }
    return render(request, 'storefront/storefront_home.html', context)

def category_products(request, category_id):
    categories = get_object_or_404(Category, id=category_id)
    products = Product.objects.all()
    sort_option = request.GET.get('sort', 'default')
    customer, created = Customer.objects.get_or_create(user=request.user)
    cart, created = Cart.objects.get_or_create(customer=customer)
    cart_items = cart.cart_items.all()
    cart_items_count = len(cart_items)
    cart_subtotal = cart.get_subtotal()
    if sort_option == 'price_asc':
        products = products.order_by('sell_price')
    elif sort_option == 'price_desc':
        products = products.order_by('-sell_price')
    elif sort_option == 'name_asc':
        products = products.order_by('name')
    elif sort_option == 'name_desc':
        products = products.order_by('-name')
    else:
        products = products.order_by('name')
    context = {
        'categories': categories,
        'cart_items': cart_items,
        'cart_items_count': cart_items_count,
        'cart_subtotal': cart_subtotal,
        'products': products
    }
    return render(request, 'storefront/category_products.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if ManagerProfile.objects.filter(user=user).exists():
                return redirect('manager_dashboard')
            else:
                customer = Customer.objects.get(user=user)
                cart, created = Cart.objects.get_or_create(customer=customer)
                return redirect('storefront_home')
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'storefront/login.html')
    return render(request, 'storefront/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()
        email = request.POST['email'].strip()
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone = request.POST['phone_number'].strip()
        address = request.POST['address'].strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        # Check if passwords match or not
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return render(request, 'storefront/register.html')

        #Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return render(request, 'storefront/register.html')

        #Check if email already in use
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use")
            return render(request, 'storefront/register.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
            is_staff=False
        )
        customer = Customer.objects.get(user=user)
        customer.phone = phone
        customer.address = address
        customer.save()
        login(request, user) #This login is builtin django function that works something like the SUPER GLOBAL VARIABLE in PHP
        cart, created = Cart.objects.get_or_create(customer=customer)
        return redirect('storefront_home')
    return render(request, 'storefront/register.html')

@login_required
def logout_user(request):
    logout(request)
    return redirect('storefront_home')

@login_required
@require_POST
def add_to_cart(request, product_id):
    if request.user.is_superuser:
        messages.error(request, "Manager can not perform this task!")
        return redirect('category_products', get_object_or_404(Product, id=product_id).category.id)

    user = request.user
    customer = get_object_or_404(Customer, user=user)
    cart, created = Cart.objects.get_or_create(customer=customer)
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    category_id = product.category.id

    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1
    except ValueError:
        quantity = 1

    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity

    cart_item.save()
    messages.success(request, f"{quantity} {product.name} added to the cart.")
    return redirect('category_products', category_id)

@login_required
def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect(request.META.get('HTTP_REFERER', 'cart'))

@login_required
def buy_now(request):
    pass

@login_required
def account_info(request):
    user = request.user
    customer, created = Customer.objects.get_or_create(user=user)
    completed = Order.objects.filter(customer=customer, status='completed').count()
    pending = Order.objects.filter(customer=customer, status='pending').count()
    cancelled = Order.objects.filter(customer=customer, status='cancelled').count()
    context = {
        'completed': completed,
        'pending': pending,
        'cancelled': cancelled,
        'customer': customer
    }
    return render(request, 'storefront/account_info.html', context)

@never_cache
@login_required
def update_profile(request):
    form = None
    if request.method == 'POST':
        form = ProfileForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('account_info')
    else:
        form = ProfileForm(user=request.user)
    return render(request, 'storefront/update_profile.html', {'form': form})


@login_required
def change_password(request):
    form = None
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('account_info')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'storefront/change_password.html', {'form': form})

