from django.contrib import admin
from .models import Sale, SaleItem

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price_at_sale', 'subtotal']

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['receipt_number', 'cashier', 'total_amount', 'created_at']
    list_filter = ['created_at']
    search_fields = ['receipt_number']
    readonly_fields = ['receipt_number', 'created_at']
    inlines = [SaleItemInline]

@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ['sale', 'product', 'quantity', 'price_at_sale', 'subtotal']
    list_filter = ['sale__created_at']
    search_fields = ['product__name', 'sale__receipt_number']
