from django.contrib.auth import get_user_model

User = get_user_model()

# Delete existing admin if exists
User.objects.filter(username='admin').delete()

# Create admin user
admin = User.objects.create_superuser(
    username='admin',
    email='admin@example.com',
    password='admin',
    role='admin'
)
print(f'Created admin user: {admin.username}')

# Delete existing cashier if exists
User.objects.filter(username='cashier').delete()

# Create cashier user
cashier = User.objects.create_user(
    username='cashier',
    email='cashier@example.com',
    password='cashier',
    role='cashier'
)
print(f'Created cashier user: {cashier.username}')

# Create sample category and products
from rms_pos.inventory.models import Category, Product

# Delete existing data
Category.objects.all().delete()

# Create categories
electronics = Category.objects.create(
    name='Electronics',
    description='Electronic items and gadgets'
)

groceries = Category.objects.create(
    name='Groceries',
    description='Food and household items'
)

print(f'Created categories: {Category.objects.count()}')

# Create sample products
Product.objects.create(
    name='Laptop',
    category=electronics,
    barcode='1234567890',
    price=999.99,
    cost=750.00,
    stock_quantity=10
)

Product.objects.create(
    name='Mouse',
    category=electronics,
    barcode='0987654321',
    price=29.99,
    cost=15.00,
    stock_quantity=50
)

Product.objects.create(
    name='Milk 1L',
    category=groceries,
    barcode='1111111111',
    price=3.99,
    cost=2.50,
    stock_quantity=100
)

Product.objects.create(
    name='Bread',
    category=groceries,
    barcode='2222222222',
    price=2.99,
    cost=1.50,
    stock_quantity=75
)

print(f'Created products: {Product.objects.count()}')
print('Setup complete!')
