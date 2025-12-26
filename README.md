# Retail Management System + Point of Sale

A full-featured retail management system with integrated POS built with Django and optimized for production with a premium, responsive UI and cloud-native architecture.

## 🚀 Recent Updates
- **PostgreSQL Migration**: Fully migrated from SQLite to high-performance PostgreSQL (hosted on Neon.tech).
- **Vercel Deployment**: Configured with optimized `vercel.json` and WhiteNoise for seamless cloud hosting.
- **Enhanced UI Persistence**: Fixed theme toggling (Dark/Light) with instant navbar access and Google Fonts (Outfit & Inter) for a premium look.
- **Cost-Centric Tracking**: The system now prioritizes **Cost Price** across the POS and Inventory modules for more accurate business tracking.
- **Inventory Analytics**: Smart dashboard with visual charts for sales trends, top-selling products, and stock alerts.
- **Enforced RBAC**: Strict view-level security and dynamic UI navigation based on user roles (Admin/Manager/Cashier).

## Features

- **Interactive Analytics Dashboard**: 
  - **Visual Insights**: Real-time Line charts for sales trends and Bar charts for top-selling products.
  - **Smart Alerts**: Auto-generated lists for low-stock items.
  - **KPIs**: Clickable stat cards for quick access to critical inventory data.
- **Modern Navigation**: Fixed top navbar with role-aware links (hides administrative options for Cashiers).
- **User Management System**:
  - **Role-based Access**: Admin, Manager, and Cashier permissions.
  - **Invite-only Registration**: Unique reference codes for new users (expiring codes with role assignment).
  - **Account Control**: Admins can activate/deactivate users and manage roles directly from the UI.
- **Advanced Sales History & Reporting**:
  - **Historical Trends**: Filter sales by all, daily, or monthly views.
  - **Print-ready Reports**: Styled daily and monthly sales summaries for physical filing.
  - **Transaction Tracking**: Detailed breakdown of items, payment methods (Cash/Card/UPI), and customer details.
- **Point of Sale (POS)**: Fast checkout interface showing **Cost Price** for internal transaction accuracy.
- **Multi-Theme Support**: Instant toggle between Premium Dark Mode and Clean Light Mode with preference persistence.
- **Responsive UI**: Mobile-first design ensures the dashboard, POS, and management tools work on phones, tablets, and desktops.

## Tech Stack

- **Backend**: Django 5.1 (Python 3.12)
- **Frontend**: HTML5, Custom Vanilla CSS (Glassmorphism), JavaScript (ES6+), **Chart.js**
- **Database**: **PostgreSQL** (Production) / SQLite (Local Default)
- **Deployment**: Vercel
- **Static Assets**: WhiteNoise (Compressed & Manifest-based serving)
- **Typography**: Google Fonts (Outfit for headings, Inter for body text)

## Installation & Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Database Configuration**:
   Create a `.env` file in the root directory (or set environment variables) with:
   ```env
   DATABASE_URL=your_postgresql_connection_string
   ```

3. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Collect Static Files**:
   ```bash
   python manage.py collectstatic --noinput
   ```

## Running the Application

1. **Local Development**:
   ```bash
   python manage.py runserver
   ```

2. **Vercel Deployment**:
   The project is configured for Vercel. Ensure `DATABASE_URL` is set in the Vercel project settings under "Environment Variables".

## Role-based Access Control

| Role | Permissions |
|------|-------------|
| **Admin** | Full access to Inventory, Sales Analytics, User Management, and Reference Code generation. |
| **Manager** | Full access to Inventory and Sales History. Can manage products and stock levels. |
| **Cashier** | Access to POS checkout interface and individual receipt generation. |

## Usage Guide

### User Registration (New Users)
1. **Reference Codes**: Admins generate unique codes for specific roles.
2. **Registration**: New users register using these codes to automatically gain the correct role permissions.

### Inventory & Management
1. **Dashboard**: Responsive grid with auto-scaling stat cards.
2. **Product List**: View buying **Costs** and stock levels. Advanced filtering for "Low Stock" items.

### POS & Sales
1. **Quick POS**: Rapid item entry based on **Cost Price**.
2. **Sales History**: Track revenue and download print-ready summaries.

## Project Structure
```
Retail-Management-System_Point-of-Sale/
├── manage.py
├── build.sh            # Vercel build script
├── vercel.json         # Vercel configuration
├── rms_pos/
│   ├── accounts/       # User roles & Management
│   ├── inventory/      # Product & cost tracking
│   ├── pos/            # POS logic & Sales
│   ├── static/         # Premium CSS & JS
│   └── templates/      # Base & App templates
```

---
*Developed for efficient retail operations with focus on visual excellence, cloud stability, and internal cost accuracy.*
