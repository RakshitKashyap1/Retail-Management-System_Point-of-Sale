from django.urls import path
from . import views

urlpatterns = [
    path('', views.pos_view, name='pos_dashboard'),
    path('api/products/', views.product_search_api, name='product_search_api'),
    path('api/checkout/', views.checkout_api, name='checkout_api'),
    path('sales/', views.sales_list, name='sales_list'),
]
