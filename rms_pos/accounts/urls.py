from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('users/', views.user_management_view, name='user_management'),
    path('users/create/', views.create_user_view, name='create_user'),
    path('users/<int:user_id>/toggle-active/', views.toggle_user_active_view, name='toggle_user_active'),
    path('reference-codes/generate/', views.generate_reference_code_view, name='generate_reference_code'),
    path('reference-codes/<int:code_id>/delete/', views.delete_reference_code_view, name='delete_reference_code'),
]
