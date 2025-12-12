# Quick Start Guide

## ✅ System is Running!

Your Retail Management System with POS is **up and running** at:
**http://127.0.0.1:8000/**

---

## 📝 Next Steps

### 1. Create Admin User
Since the automated script had issues, create an admin user manually:

```bash
python manage.py createsuperuser
```

Follow the prompts to set:
- Username: `admin`
- Email: `admin@example.com`
- Password: `admin123` (or your choice)
- When asked for role, the default 'cashier' will be set, you can change it in admin panel

### 2. Access the Admin Panel

Go to: **http://127.0.0.1:8000/admin/**

Login with your superuser credentials and:
1. Change your user's role to `admin` (in Users section)
2. Create some **Categories** (e.g., Electronics, Groceries)
3. Create some **Products** with:
   - Name
   - Category
   - Barcode (any unique number)
   - Price
   - Cost
   - Stock Quantity

### 3. Start Tailwind CSS (Important!)

In a **separate terminal**, run:

```bash
cd rms_pos
npm run build:css
```

This will watch for changes and compile your Tailwind CSS. Keep this running!

---

## 🎯 Using the System

### For Admin/Managers (Inventory Management)

1. **Login**: Go to http://127.0.0.1:8000/accounts/login/
2. Use your admin credentials
3. You'll be redirected to the **Inventory Dashboard**
4. From here you can:
   - View total products and low stock alerts
   - Add/Edit products
   - View inventory activity logs

**Key URLs:**
- Dashboard: http://127.0.0.1:8000/inventory/dashboard/
- Product List: http://127.0.0.1:8000/inventory/products/
- Add Product: http://127.0.0.1:8000/inventory/products/add/

### For Cashiers (POS Interface)

1. **Create a cashier user** in admin panel or:
   ```bash
   python manage.py createsuperuser
   # Set role to 'cashier' in admin panel
   ```

2. **Login** with cashier credentials
3. You'll be redirected to the **POS Interface**
4. Features:
   - Search products by name or barcode
   - Click products to add to cart
   - Adjust quantities with +/- buttons
   - Click **Checkout** to complete sale
   - Stock automatically deducts

**POS URL:**
- http://127.0.0.1:8000/pos/

---

## 🎨 Barcode Scanning

The POS search field supports barcode scanners!
- Just scan the barcode - it will auto-search
- Works with any USB barcode scanner (configured as keyboard input)

---

## 🔧 Troubleshooting

### CSS not loading?
Make sure Tailwind is running:
```bash
cd rms_pos
npm run build:css
```

### Can't login?
Create a superuser first:
```bash
python manage.py createsuperuser
```

### Images not uploading?
Pillow is installed, but make sure the `media` folder exists and has write permissions.

---

## 📊 Sample Test Flow

1. **As Admin:**
   - Create category "Electronics"
   - Add product: "Laptop", barcode "123456", price $999, stock 10

2. **As Cashier:**
   - Login to POS
   - Type "123456" or "Laptop" in search
   - Add to cart
   - Checkout

3. **Verify:**
   - Go back to inventory
   - Check stock reduced to 9
   - Check inventory log shows the sale

---

## 🚀 Production Deployment

Before deploying to production:

1. Change `DEBUG = False` in settings.py
2. Set a secure `SECRET_KEY`
3. Configure proper database (PostgreSQL recommended)
4. Set `ALLOWED_HOSTS`
5. Use a production server (Gunicorn + Nginx)
6. Build Tailwind CSS for production:
   ```bash
   npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --minify
   ```

---

**Enjoy your Retail Management System! 🎉**
