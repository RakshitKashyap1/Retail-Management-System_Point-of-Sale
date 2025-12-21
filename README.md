# Retail Management System + Point of Sale

A full-featured retail management system with integrated POS built with Django and optimized with a premium responsive UI.

## Features

- **Interactive Dashboard**: Centered overview with large, clickable stat cards for Total Products, Low Stock and Daily Sales.
- **Modern Navigation**: Fixed top navbar with a collapsible hamburger side menu and persistent brand visibility.
- **User Management System**:
  - **Role-based Access**: Admin, Manager, and Cashier permissions.
  - **Invite-only Registration**: Unique reference codes for new users (expiring codes with role assignment).
  - **Account Control**: Admins can activate/deactivate users and manage roles directly from the UI.
- **Advanced Sales History & Reporting**:
  - **Historical Trends**: Filter sales by all, daily, or monthly views.
  - **Print-ready Reports**: Styled daily and monthly sales summaries for physical filing.
  - **Transaction Tracking**: Detailed breakdown of items, payment methods (Cash/Card/UPI), and customer details.
- **Point of Sale (POS)**: Fast checkout interface that automatically hides out-of-stock items for accuracy.
- **Multi-Theme Support**: Instant toggle between Premium Dark Mode and Clean Light Mode with preference persistence.
- **Responsive UI**: Mobile-first design ensures the dashboard, POS, and management tools work on phones, tablets, and desktops.

## Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, Custom CSS (Vanilla + Glassmorphism), JavaScript
- **Icons**: SVG-based modern icon set
- **Database**: SQLite (default)

## Installation

1. **Install Python dependencies**:
   ```bash
   pip install django pillow
   ```

2. **Run migrations**:
   ```bash
   python manage.py makemigrations accounts
   python manage.py makemigrations inventory
   python manage.py makemigrations pos
   python manage.py migrate
   ```

3. **Create initial admin**:
   ```bash
   python manage.py createsuperuser
   ```

## Running the Application

1. **Start Django development server**:
   ```bash
   python manage.py runserver
   ```

2. **Access the application**:
   - Main Dashboard: http://127.0.0.1:8000/
   - User Management: http://127.0.0.1:8000/accounts/management/
   - Login: http://127.0.0.1:8000/accounts/login/

## Role-based Access Control

| Role | Permissions |
|------|-------------|
| **Admin** | Full access to Inventory, Sales Analytics, User Management, and Reference Code generation. |
| **Manager** | Full access to Inventory and Sales History. Can manage products and stock levels. |
| **Cashier** | Access to POS checkout interface and individual receipt generation. |

## Usage Guide

### User Registration (New Users)
1. **Reference Codes**: Admins generate unique codes for specific roles (Admin/Manager/Cashier).
2. **Expiry**: Codes are valid for 7 days by default.
3. **Registration**: New users register using these codes to automatically gain the correct role permissions.

### Inventory & Management
1. **Dashboard**: Fully responsive grid with auto-scaling stat cards.
2. **Product List**: Advanced filtering for "Low Stock" items to streamline replenishment.
3. **User Management**: Unified dashboard to manage active accounts and track user creation history.

### POS & Sales
1. **Quick POS**: Rapid item entry with automatic out-of-stock filtering.
2. **Payment Processing**: Integrated change calculator for cash and confirmation for UPI/Card.
3. **Sales History**: Print-ready daily/monthly summaries with timestamped reporting.

## Project Structure

```
Retail-Management-System_Point-of-Sale/
├── manage.py
├── rms_pos/
│   ├── accounts/         # User roles, Reference codes & Management
│   ├── inventory/        # Product & stock management
│   ├── pos/              # POS logic & Sales tracking
│   ├── templates/        # Unified templates with base.html layout
│   │   ├── accounts/     # User mgmt & Registration
│   │   ├── inventory/    # Responsive Dashboard
│   │   └── pos/          # POS & Sales reports
│   ├── static/           # CSS (Theme engine) & JS (Menu logic)
│   └── media/            # Product images
```

---
*Developed for efficient retail operations with focus on visual excellence and operational speed.*

