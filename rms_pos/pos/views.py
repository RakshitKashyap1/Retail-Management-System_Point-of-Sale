from django.shortcuts import render, get_object_or_404
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
    products = Product.objects.filter(
        name__icontains=query
    ) | Product.objects.filter(
        barcode__icontains=query
    )
    results = []
    for p in products[:50]:
        discounted_price = p.get_discounted_price()
        results.append({
            'id': p.id,
            'name': p.name,
            'price': float(p.price),
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
            
            discounted_price = product.get_discounted_price()
            discount_amount_per_unit = product.price - discounted_price
            
            SaleItem.objects.create(
                sale=sale,
                product=product,
                quantity=quantity,
                price_at_sale=discounted_price,
                subtotal=discounted_price * quantity
            )
            
            total_amount += float(discounted_price) * quantity
            total_discount += float(discount_amount_per_unit) * quantity

        sale.total_amount = total_amount
        sale.discount_amount = total_discount
        sale.save()
        
        return JsonResponse({'success': True, 'receipt_number': sale.receipt_number})
        
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def sales_list(request):
    sales = Sale.objects.prefetch_related('items__product').select_related('cashier').order_by('-created_at')
    return render(request, 'pos/sales_list.html', {'sales': sales})
