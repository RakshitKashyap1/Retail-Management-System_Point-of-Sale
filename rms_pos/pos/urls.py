from django.urls import path
from . import views

urlpatterns = [
    path('', views.pos_view, name='pos_dashboard'),
    path('api/products/', views.product_search_api, name='product_search_api'),
    path('api/checkout/', views.checkout_api, name='checkout_api'),
    path('payment/<int:sale_id>/', views.payment_page, name='payment_page'),
    path('api/payment/<int:sale_id>/process/', views.process_payment, name='process_payment'),
    path('receipt/<int:sale_id>/', views.receipt_page, name='receipt_page'),
    path('api/receipt/<int:sale_id>/customer/', views.save_customer_details, name='save_customer_details'),
    path('sales/', views.sales_list, name='sales_list'),
    path('sales/export/', views.export_sales_data, name='export_sales_data'),
    path('customers/', views.customers_list, name='customers_list'),
]

