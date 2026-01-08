# Retail Management System + Point of Sale

A full-featured retail management system with integrated POS built with Django and optimized for production with a premium, responsive UI and cloud-native architecture.

## 🚀 Recent Updates

- **Smart Accounting Integration**: Added full export capability for Sales, Product performance, and Customer data to CSV (Excel-compatible) for offline accounting and secondary analysis.
- **Payment & Checkout Flow**: Enhanced POS with multi-payment support (Cash, Card, UPI), automatic change calculation, and receipt generation.
- **Customer CRM & Loyalty**: Integrated customer data capture (Name/Mobile) post-checkout to track repeat customers and build loyalty logs.
- **Sales Targets & KPIs**: Implement role-based and team-wide sales targets with real-time progress tracking on the dashboard.
- **PostgreSQL Migration**: Fully migrated from SQLite to high-performance PostgreSQL (hosted on Neon.tech).
- **Vercel Deployment**: Configured with optimized `vercel.json` and WhiteNoise for seamless cloud hosting.
- **Enhanced UI Persistence**: Fixed theme toggling (Dark/Light) with instant navbar access and Google Fonts (Outfit & Inter) for a premium look.
- **Offline Synchronization**: Engineered for reliability with support for local PostgreSQL replication and synchronization with production cloud databases.
- **Enforced RBAC**: Strict view-level security and dynamic UI navigation based on user roles (Admin/Manager/Cashier).

## 🌟 Key Features

### 📊 Interactive Analytics Dashboard
- **Visual Insights**: Real-time Line charts for sales trends and Bar charts for top-selling products using **Chart.js**.
- **Sales Targets**: Active progress bars for individual and team sales targets.
- **Smart Alerts**: Auto-generated lists for low-stock items.
- **KPIs**: Clickable stat cards for quick access to critical inventory data.

### 🛒 Advanced Point of Sale (POS)
- **Fast Checkout**: Rapid item entry with real-time search and stock validation.
- **Multi-Payment Support**: Seamlessly handle Cash, Card, and UPI transactions.
- **Transaction Details**: Integrated receipt generation with unique receipt numbers.
- **Cost-Centric Tracking**: System prioritizes **Cost Price** across modules for internal accuracy.

### 👥 User Management & CRM
- **Role-based Access**: Custom decorators for Admin, Manager, and Cashier permissions.
- **Invite-only Registration**: Unique reference codes for new users with expiring links.
- **Customer Analytics**: Track customer visits, total spend, and contact details for CRM.

### 📄 Reporting & Portability
- **Historical Trends**: Filter sales by Daily, Monthly, or Product-wise performance.
- **Data Export**: One-click Export to CSV for all major modules (Sales, Products, Customers).
- **Print-ready Reports**: Styled summaries for physical filing and auditing.

### 🎨 Premium UI/UX
- **Multi-Theme Support**: Instant toggle between Premium Dark Mode and Clean Light Mode with preference persistence.
- **Responsive Design**: Mobile-first architecture ensuring full functionality on phones, tablets, and desktops.
- **Modern Typography**: Powered by Google Fonts (Outfit & Inter) for a professional look.

## 🛠 Tech Stack

- **Backend**: Django 5.1 (Python 3.12)
- **Frontend**: HTML5/CSS3 (Glassmorphism), JavaScript (ES6+), **Chart.js**
- **Database**: **PostgreSQL** (Production & Local) / SQLite (Development Fallback)
- **Static Assets**: WhiteNoise (Compressed & Manifest-based serving)
- **Deployment**: Vercel

## ⚙️ Installation & Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Database Configuration**:
   Create a `.env` file in the root directory (using `.env.example` as a template):
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

5. **Seed Sample Data (Optional)**:
   ```bash
   python create_sample_data.py
   python create_users.py
   ```

## 🚀 Running the Application

1. **Local Development**:
   ```bash
   python manage.py runserver
   ```

2. **Vercel Deployment**:
   The project is configured for Vercel. Ensure `DATABASE_URL` is set in the Vercel project settings.

### 🔄 Database Synchronization

For environments requiring local/remote sync:
1. Configure `ONLINE_DATABASE_URL` and `LOCAL_DATABASE_URL` in `.env`.
2. Run the sync script:
   ```bash
   python sync_db.py
   ```

## 🛡 Role-based Access Control

| Role | Permissions |
|------|-------------|
| **Admin** | Full system access: Inventory, Analytics, User Management, and Reference Codes. |
| **Manager** | Management access: Inventory, Sales History, Product editing, and Dashboards. |
| **Cashier** | Operations access: POS interface and individual receipt generation. |

## 📁 Project Structure

```
Retail-Management-System_Point-of-Sale/
├── rms_pos/
│   ├── core/           # Decorators & Shared logic
│   ├── accounts/       # User roles & Registration
│   ├── inventory/      # Product, Categories & Analytics
│   ├── pos/            # POS, Sales & CRM
│   ├── static/         # Premium CSS & JS Assets
│   └── templates/      # Base, Layouts & App templates
├── manage.py
├── sync_db.py          # Database synchronization script
├── build.sh            # Vercel deployment script
├── vercel.json         # Vercel configuration
└── requirements.txt    # Project dependencies
```

---
*Developed for efficient retail operations with focus on visual excellence, cloud stability, and internal cost accuracy.*
