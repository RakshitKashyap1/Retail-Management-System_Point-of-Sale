from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, F
from django.db.models.functions import TruncMonth, TruncDay
from django.utils import timezone
from django.http import JsonResponse
from .models import Product, Category, InventoryLog
from .forms import ProductForm
from core.decorators import manager_required

@login_required
@manager_required
def dashboard(request):
    from pos.models import Sale, SaleItem
    
    today = timezone.now().date()
    daily_sales = Sale.objects.filter(created_at__date=today).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    total_products = Product.objects.count()
    low_stock_count = Product.objects.filter(stock_quantity__lte=10).count()
    
    # Top Selling Products Logic for Template (optional, can be loaded via API)
    top_selling = SaleItem.objects.values('product__name')\
        .annotate(total_qty=Sum('quantity'))\
        .order_by('-total_qty')[:5]

    context = {
        'total_products': total_products,
        'low_stock': low_stock_count,
        'daily_sales': daily_sales,
        'top_selling': top_selling
    }
    return render(request, 'inventory/dashboard.html', context)

@login_required
@manager_required
def dashboard_analytics_api(request):
    """API endpoint for dashboard charts"""
    from pos.models import Sale, SaleItem
    import datetime
    
    # 1. Top Selling Products
    top_products = SaleItem.objects.values('product__name')\
        .annotate(total_qty=Sum('quantity'))\
        .order_by('-total_qty')[:5]
        
    top_products_data = {
        'labels': [item['product__name'] for item in top_products],
        'data': [item['total_qty'] for item in top_products]
    }
    
    # 2. Low Stock Alerts
    low_stock_items = Product.objects.filter(stock_quantity__lte=10).values('name', 'stock_quantity')[:10]
    low_stock_data = {
        'labels': [item['name'] for item in low_stock_items],
        'data': [item['stock_quantity'] for item in low_stock_items]
    }

    # 3. Seasonal Trends (Last 7 Days Sales)
    last_7_days = timezone.now().date() - datetime.timedelta(days=7)
    sales_trend = Sale.objects.filter(created_at__date__gte=last_7_days)\
        .annotate(day=TruncDay('created_at'))\
        .values('day')\
        .annotate(total=Sum('total_amount'))\
        .order_by('day')
        
    sales_trend_data = {
        'labels': [item['day'].strftime('%Y-%m-%d') for item in sales_trend],
        'data': [float(item['total']) for item in sales_trend]
    }
    
    return JsonResponse({
        'top_products': top_products_data,
        'low_stock': low_stock_data,
        'sales_trend': sales_trend_data
    })

@login_required
@manager_required
def product_list(request):
    status = request.GET.get('stock_status', 'all')
    products = Product.objects.select_related('category').all()
    
    if status == 'low':
        products = products.filter(stock_quantity__lte=10)
        title = 'Low Stock Items'
    elif status == 'instock':
        products = products.filter(stock_quantity__gt=10)
        title = 'In-Stock Items'
    else:
        title = 'All Products'
        
    return render(request, 'inventory/product_list.html', {
        'products': products,
        'current_status': status,
        'title': title
    })

@login_required
@manager_required
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
@manager_required
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
@login_required
@manager_required
def export_products_data(request):
    import csv
    from django.http import HttpResponse

    status = request.GET.get('stock_status', 'all')
    products = Product.objects.select_related('category').all()
    filename = "products_all"

    if status == 'low':
        products = products.filter(stock_quantity__lte=10)
        filename = "products_low_stock"
    elif status == 'instock':
        products = products.filter(stock_quantity__gt=10)
        filename = "products_in_stock"
        
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'Category', 'Barcode', 'Cost', 'Discount (%)', 'Stock Quantity'])
    
    for product in products:
        writer.writerow([
            product.name,
            product.category.name if product.category else 'Uncategorized',
            product.barcode,
            product.cost,
            product.discount_percentage,
            product.stock_quantity
        ])
        
    return response
