import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rms_pos.settings')
django.setup()

from inventory.models import Category, Product

# Create categories
print('Creating categories...')
electronics, _ = Category.objects.get_or_create(
    name='Electronics',
    defaults={'description': 'Electronic items and gadgets'}
)

groceries, _ = Category.objects.get_or_create(
    name='Groceries',
    defaults={'description': 'Food and household items'}
)

clothing, _ = Category.objects.get_or_create(
    name='Clothing',
    defaults={'description': 'Apparel and accessories'}
)

print(f'✅ Categories: {Category.objects.count()}')

# Create sample products
print('\nCreating sample products...')

products_data = [
    {
        'name': 'Laptop',
        'category': electronics,
        'barcode': '1234567890',
        'price': 999.99,
        'cost': 750.00,
        'stock_quantity': 10
    },
    {
        'name': 'Wireless Mouse',
        'category': electronics,
        'barcode': '0987654321',
        'price': 29.99,
        'cost': 15.00,
        'stock_quantity': 50
    },
    {
        'name': 'USB Keyboard',
        'category': electronics,
        'barcode': '1111111111',
        'price': 49.99,
        'cost': 25.00,
        'stock_quantity': 30
    },
    {
        'name': 'Milk 1L',
        'category': groceries,
        'barcode': '2222222222',
        'price': 3.99,
        'cost': 2.50,
        'stock_quantity': 100
    },
    {
        'name': 'Bread Loaf',
        'category': groceries,
        'barcode': '3333333333',
        'price': 2.99,
        'cost': 1.50,
        'stock_quantity': 75
    },
    {
        'name': 'Coffee Beans 500g',
        'category': groceries,
        'barcode': '4444444444',
        'price': 12.99,
        'cost': 8.00,
        'stock_quantity': 40
    },
    {
        'name': 'T-Shirt',
        'category': clothing,
        'barcode': '5555555555',
        'price': 19.99,
        'cost': 10.00,
        'stock_quantity': 60
    },
    {
        'name': 'Jeans',
        'category': clothing,
        'barcode': '6666666666',
        'price': 49.99,
        'cost': 30.00,
        'stock_quantity': 25
    },
]

for product_data in products_data:
    product, created = Product.objects.get_or_create(
        barcode=product_data['barcode'],
        defaults=product_data
    )
    if created:
        print(f'  + {product.name} (${product.price})')

print(f'\n✅ Products: {Product.objects.count()}')
print('\n✅ Sample data created successfully!')
