from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db import transaction
import json
from inventory.models import Product, InventoryLog
from .models import Sale, SaleItem

@login_required
def pos_view(request):
    return render(request, 'pos/index.html')

@login_required
def product_search_api(request):
    query = request.GET.get('q', '')
    products = (Product.objects.filter(
        name__icontains=query,
        stock_quantity__gt=0
    ) | Product.objects.filter(
        barcode__icontains=query,
        stock_quantity__gt=0
    )).order_by('-discount_percentage', 'name')
    results = []
    for p in products[:50]:
        discounted_price = p.get_discounted_price()
        results.append({
            'id': p.id,
            'name': p.name,
            'price': float(p.price),
            'cost': float(p.cost),
            'discounted_price': float(discounted_price),
            'discount_percentage': float(p.discount_percentage),
            'stock': p.stock_quantity,
            'barcode': p.barcode,
            'image_url': p.image.url if p.image else None
        })
    return JsonResponse({'results': results})

@login_required
@require_POST
@transaction.atomic
def checkout_api(request):
    try:
        data = json.loads(request.body)
        cart = data.get('cart', [])
        
        if not cart:
            return JsonResponse({'error': 'Cart is empty'}, status=400)

        total_amount = 0
        total_discount = 0
        sale = Sale.objects.create(
            cashier=request.user,
            total_amount=0 # Will update later
        )

        for item in cart:
            product_id = item.get('id')
            quantity = int(item.get('quantity', 1))
            
            product = Product.objects.select_for_update().get(id=product_id)
            
            if product.stock_quantity < quantity:
                raise ValueError(f"Insufficient stock for {product.name}")
            
            product.stock_quantity -= quantity
            product.save()
            
            InventoryLog.objects.create(
                product=product,
                action='sale',
                quantity=quantity,
                user=request.user,
                note=f"Sale {sale.receipt_number}"
            )
            
            # Use cost instead of price for the sale
            sale_price = product.cost
            
            SaleItem.objects.create(
                sale=sale,
                product=product,
                quantity=quantity,
                price_at_sale=sale_price,
                subtotal=sale_price * quantity
            )
            
            total_amount += float(sale_price) * quantity
            # We skip discount calculation here since we're selling at cost

        sale.total_amount = total_amount
        sale.discount_amount = total_discount
        sale.save()
        
        return JsonResponse({'success': True, 'sale_id': sale.id, 'receipt_number': sale.receipt_number})
        
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def payment_page(request, sale_id):
    """Display payment options page"""
    from django.shortcuts import redirect
    sale = get_object_or_404(Sale, id=sale_id, cashier=request.user)
    
    if sale.is_completed:
        # If already completed, redirect to receipt
        return redirect('receipt_page', sale_id=sale.id)
    
    items = sale.items.select_related('product').all()
    
    return render(request, 'pos/payment.html', {
        'sale': sale,
        'items': items
    })

@login_required
@require_POST
def process_payment(request, sale_id):
    """Process the payment and complete the sale"""
    sale = get_object_or_404(Sale, id=sale_id, cashier=request.user)
    
    if sale.is_completed:
        return JsonResponse({'error': 'Sale already completed'}, status=400)
    
    try:
        data = json.loads(request.body)
        payment_method = data.get('payment_method', 'cash')
        
        sale.payment_method = payment_method
        
        if payment_method == 'cash':
            cash_received = float(data.get('cash_received', 0))
            if cash_received < float(sale.total_amount):
                return JsonResponse({'error': 'Insufficient cash received'}, status=400)
            
            sale.cash_received = cash_received
            sale.change_amount = cash_received - float(sale.total_amount)
        
        sale.is_completed = True
        sale.save()
        
        return JsonResponse({
            'success': True,
            'sale_id': sale.id,
            'receipt_number': sale.receipt_number
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def receipt_page(request, sale_id):
    """Display receipt with option to add customer details"""
    sale = get_object_or_404(Sale, id=sale_id)
    items = sale.items.select_related('product').all()
    
    return render(request, 'pos/receipt.html', {
        'sale': sale,
        'items': items
    })

@login_required
@require_POST
def save_customer_details(request, sale_id):
    """Save customer details for loyalty program"""
    sale = get_object_or_404(Sale, id=sale_id)
    
    try:
        data = json.loads(request.body)
        customer_name = data.get('customer_name', '').strip()
        customer_mobile = data.get('customer_mobile', '').strip()
        
        sale.customer_name = customer_name
        sale.customer_mobile = customer_mobile
        sale.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Customer details saved successfully'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def sales_list(request):
    sales = Sale.objects.filter(is_completed=True).prefetch_related('items__product').select_related('cashier').order_by('-created_at')
    
    view_type = request.GET.get('view', 'all')
    date_input = request.GET.get('date')
    month_input = request.GET.get('month')
    
    if view_type == 'daily' and date_input:
        sales = sales.filter(created_at__date=date_input)
    elif view_type == 'monthly' and month_input:
        year, month = month_input.split('-')
        sales = sales.filter(created_at__year=year, created_at__month=month)
        
    total_sales = sales.aggregate(total=Sum('total_amount'))['total'] or 0
    
    return render(request, 'pos/sales_list.html', {
        'sales': sales,
        'view_type': view_type,
        'selected_date': date_input,
        'selected_month': month_input,
        'total_sales': total_sales
    })

@login_required
def export_sales_data(request):
    import csv
    from django.http import HttpResponse

    sales = Sale.objects.filter(is_completed=True).prefetch_related('items__product').select_related('cashier').order_by('-created_at')
    
    view_type = request.GET.get('view', 'all')
    date_input = request.GET.get('date')
    month_input = request.GET.get('month')
    
    filename = "sales_web_export"

    if view_type == 'daily' and date_input:
        sales = sales.filter(created_at__date=date_input)
        filename = f"sales_daily_{date_input}"
    elif view_type == 'monthly' and month_input:
        year, month = month_input.split('-')
        sales = sales.filter(created_at__year=year, created_at__month=month)
        filename = f"sales_monthly_{month_input}"
        
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Receipt Number', 'Date', 'Time', 'Cashier', 'Customer Name', 'Customer Mobile', 'Payment Method', 'Total Amount', 'Items'])
    
    for sale in sales:
        items_str = ", ".join([f"{item.quantity}x {item.product.name}" for item in sale.items.all()])
        
        writer.writerow([
            sale.receipt_number,
            sale.created_at.strftime('%Y-%m-%d'),
            sale.created_at.strftime('%H:%M:%S'),
            sale.cashier.username if sale.cashier else 'Unknown',
            sale.customer_name,
            sale.customer_mobile,
            sale.get_payment_method_display(),
            sale.total_amount,
            items_str
        ])
        
    return response
