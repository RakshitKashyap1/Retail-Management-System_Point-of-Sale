from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='inventory_dashboard'),
    path('dashboard/api/analytics/', views.dashboard_analytics_api, name='dashboard_analytics_api'),
    path('products/', views.product_list, name='product_list'),

    path('products/add/', views.add_product, name='add_product'),
    path('products/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('products/export/', views.export_products_data, name='export_products_data'),
]
