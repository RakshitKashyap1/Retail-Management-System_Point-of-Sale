from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def admin_required(function=None):
    """
    Decorator for views that checks that the user is logged in and is an admin.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and (u.is_superuser or u.is_admin()),
        login_url='login',
        redirect_field_name=None
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def manager_required(function=None):
    """
    Decorator for views that checks that the user is logged in and is a manager or admin.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and (u.is_superuser or u.is_admin() or u.is_manager()),
        login_url='login',
        redirect_field_name=None
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def cashier_required(function=None):
    """
    Decorator for views that checks that the user is logged in and is a cashier, manager, or admin.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and (u.is_superuser or u.is_admin() or u.is_manager() or u.is_cashier()),
        login_url='login',
        redirect_field_name=None
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
