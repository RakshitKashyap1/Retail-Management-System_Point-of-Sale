# Retail Management System + Point of Sale

A full-featured retail management system with integrated POS built with Django and optimized with a premium dark UI.

## Features

- **Interactive Dashboard**: Centered overview with large, clickable stat cards for Total Products, Low Stock and Daily Sales.
- **Advanced Filtering**: Quick-toggle pill-style filters on the product list (All, In Stock, Low Stock).
- **Point of Sale (POS)**: Fast checkout interface that automatically hides out-of-stock items for accuracy.
- **Daily Performance**: Real-time tracking of daily revenue and sales volume on the admin dashboard.
- **Dynamic Stock Alerts**: Visual stock level badges and dedicated replenishment filters.
- **Premium UI**: Modern dark theme with glassmorphism, scaled-up statistics, and high-contrast visuals.
- **Role-based Security**: Automated redirects and permission levels for Admin, Manager, and Cashier.

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
| **Admin** | Full access to Inventory, Analytics Dashboard, and User Management. |
| **Manager** | Access to Inventory Dashboard and Product Management. |
| **Cashier** | Access to POS interface only. |

*Note: The default superuser created via `createsuperuser` has full admin access.*

## Usage Guide

### Analytics & Inventory (Admin/Manager)
1. **Dashboard Overview**: View "Daily Sales" revenue and "Low Stock" counts at a glance.
2. **Interactive Stats**: Click on any dashboard card to jump directly to the detailed view.
3. **Smart Inventory**: Use the specialized filters (In Stock / Low Stock) to manage replenishment.
4. **Product Management**: Add or edit products with images, barcodes, and automated inventory logging.

### POS Operations (Cashier)
1. **Search**: Find products rapidly by name or by scanning a barcode.
2. **Automated Stock Protection**: Items with zero stock are hidden to prevent invalid sales.
3. **Cart Management**: Adjust quantities, remove items, and see real-time price totals with discounts.
4. **Checkout**: Secure transaction processing with automatic stock deduction and receipt generation.


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
