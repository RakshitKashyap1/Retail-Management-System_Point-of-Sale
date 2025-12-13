# Retail Management System + Point of Sale

A full-featured retail management system with integrated POS built with Django and optimized with a premium dark UI.

## Features

- **Inventory Management**: Manage products, categories, and stock levels.
- **Point of Sale (POS)**: Fast checkout interface with barcode scanning support.
- **Real-time Stock Sync**: Automatic stock updates on every sale.
- **Role-based Authentication**: Admin, Manager, and Cashier roles.
- **Barcode Support**: Scan or search products by barcode.
- **Premium UI**: Modern, responsive dark theme with glassmorphism effects.
- **Sales History**: View past receipts and sales details.

## Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, Custom CSS (Vanilla + Glassmorphism), JavaScript
- **Database**: SQLite (default)

## Installation

1. **Install Python dependencies**:
   ```bash
   pip install django pillow
   ```

2. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create superuser** (if not already created):
   ```bash
   python manage.py createsuperuser
   ```

## Running the Application

1. **Start Django development server**:
   ```bash
   python manage.py runserver
   ```

2. **Access the application**:
   - Main app: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/
   - Login: http://127.0.0.1:8000/accounts/login/

## Default Credentials / Roles

You can create users with different roles in the Admin Panel.

| Role | Permissions |
|------|-------------|
| **Admin** | Full access to Inventory, POS, and User Management. |
| **Cashier** | Access to POS interface only. |

*Note: The default superuser created via `createsuperuser` has full admin access.*

## Usage Guide

### Inventory Management (Admin/Manager)
1. Login with admin credentials.
2. Navigate to Inventory Dashboard.
3. Add categories and products (images, prices, stock).
4. View recent inventory activity.

### POS Interface (Cashier)
1. Login with cashier credentials.
2. Search for products by name or scan barcode.
3. Add items to cart.
4. Adjust quantities as needed.
5. Click **Checkout** to complete sale.
6. Stock is automatically deducted.

## Project Structure

```
Retail Management System + Point of Sale/
├── manage.py
├── rms_pos/
│   ├── settings.py
│   ├── urls.py
│   ├── accounts/         # User authentication
│   ├── inventory/        # Product & stock management
│   ├── pos/              # Point of sale interface
│   ├── core/             # Core utilities
│   ├── templates/        # HTML templates
│   ├── static/           # Static files (CSS, JS, Images)
│   └── media/            # Uploaded files (Product images)
```
