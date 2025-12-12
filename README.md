# Retail Management System + Point of Sale

A full-featured retail management system with integrated POS built with Python Django framework.

## Features

- **Inventory Management**: Manage products, categories, and stock levels
- **Point of Sale (POS)**: Fast checkout interface with barcode scanning support
- **Real-time Stock Sync**: Automatic stock updates on every sale
- **Role-based Authentication**: Admin, Manager, and Cashier roles
- **Barcode Support**: Scan or search products by barcode

## Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS
- **Database**: SQLite (can be switched to PostgreSQL/MySQL)

## Installation

1. **Install Python dependencies**:
   ```bash
   pip install django pillow
   ```

2. **Install Node dependencies** (for Tailwind CSS):
   ```bash
   cd rms_pos
   npm install
   ```

3. **Run migrations**:
   ```bash
   cd ..
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create superuser** (if not already created):
   ```bash
   python manage.py createsuperuser
   ```

## Running the Application

1. **Start Tailwind CSS build process** (in one terminal):
   ```bash
   cd rms_pos
   npm run build:css
   ```

2. **Start Django development server** (in another terminal):
   ```bash
   cd ..
   python manage.py runserver
   ```

3. **Access the application**:
   - Main app: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/
   - Login: http://127.0.0.1:8000/accounts/login/

## Default Credentials

- **Admin**: username: `admin`, password: `admin`
- **Cashier**: username: `cashier`, password: `cashier`

## Usage Guide

### Inventory Management (Admin/Manager)

1. Login with admin credentials
2. Navigate to Inventory Dashboard
3. Add categories and products
4. Set barcodes, prices, and stock quantities
5. View recent inventory activity

### POS Interface (Cashier)

1. Login with cashier credentials
2. Search for products by name or scan barcode
3. Add items to cart
4. Adjust quantities as needed
5. Click Checkout to complete sale
6. Stock is automatically deducted

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
│   ├── static/           # Static files
│   └── media/            # Uploaded files
└── static/               # Project-level static files
```


