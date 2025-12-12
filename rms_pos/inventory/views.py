from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Product, Category, InventoryLog
from .forms import ProductForm

def is_manager_or_admin(user):
    return user.is_authenticated and (user.is_manager() or user.is_admin())

@login_required
@user_passes_test(is_manager_or_admin)
def dashboard(request):
    total_products = Product.objects.count()
    low_stock = Product.objects.filter(stock_quantity__lte=10).count()
    recent_logs = InventoryLog.objects.select_related('product', 'user').order_by('-timestamp')[:10]
    
    context = {
        'total_products': total_products,
        'low_stock': low_stock,
        'recent_logs': recent_logs,
    }
    return render(request, 'inventory/dashboard.html', context)

@login_required
@user_passes_test(is_manager_or_admin)
def product_list(request):
    products = Product.objects.select_related('category').all()
    return render(request, 'inventory/product_list.html', {'products': products})

@login_required
@user_passes_test(is_manager_or_admin)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            InventoryLog.objects.create(
                product=product,
                action='add',
                quantity=product.stock_quantity,
                user=request.user,
                note='Initial stock'
            )
            messages.success(request, 'Product added successfully.')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'inventory/product_form.html', {'form': form, 'title': 'Add Product'})

@login_required
@user_passes_test(is_manager_or_admin)
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            old_stock = Product.objects.get(pk=pk).stock_quantity
            product = form.save()
            new_stock = product.stock_quantity
            if new_stock != old_stock:
                diff = new_stock - old_stock
                action = 'add' if diff > 0 else 'remove'
                InventoryLog.objects.create(
                    product=product,
                    action=action,
                    quantity=abs(diff),
                    user=request.user,
                    note='Manual update'
                )
            messages.success(request, 'Product updated successfully.')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory/product_form.html', {'form': form, 'title': 'Edit Product'})
