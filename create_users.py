import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rms_pos.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create admin user
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin',
        role='admin'
    )
    print(f'✅ Created admin user: {admin.username} (password: admin)')
else:
    print('ℹ️  Admin user already exists')

# Create cashier user
if not User.objects.filter(username='cashier').exists():
    cashier = User.objects.create_user(
        username='cashier',
        email='cashier@example.com',
        password='cashier',
        role='cashier'
    )
    print(f'✅ Created cashier user: {cashier.username} (password: cashier)')
else:
    print('ℹ️  Cashier user already exists')

# Create manager user
if not User.objects.filter(username='manager').exists():
    manager = User.objects.create_user(
        username='manager',
        email='manager@example.com',
        password='manager',
        role='manager'
    )
    print(f'✅ Created manager user: {manager.username} (password: manager)')
else:
    print('ℹ️  Manager user already exists')

print('\n✅ Setup complete!')
print('\nCredentials:')
print('  Admin:    username=admin,    password=admin')
print('  Manager:  username=manager,  password=manager')
print('  Cashier:  username=cashier,  password=cashier')
