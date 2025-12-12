from django.contrib import admin
from .models import Category, Product, InventoryLog

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'barcode', 'price', 'cost', 'stock_quantity']
    list_filter = ['category']
    search_fields = ['name', 'barcode']
    list_editable = ['price', 'stock_quantity']

@admin.register(InventoryLog)
class InventoryLogAdmin(admin.ModelAdmin):
    list_display = ['product', 'action', 'quantity', 'user', 'timestamp']
    list_filter = ['action', 'timestamp']
    search_fields = ['product__name']
    readonly_fields = ['timestamp']
