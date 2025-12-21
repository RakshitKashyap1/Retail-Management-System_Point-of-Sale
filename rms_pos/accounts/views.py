from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import User, ReferenceCode
from .forms import RegistrationForm, CreateUserForm, GenerateReferenceCodeForm


def register_view(request):
    """Handle new user registration with reference code"""
    if request.user.is_authenticated:
        return redirect('inventory_dashboard')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created successfully! Welcome, {user.username}. You can now login.')
            return redirect('login')
    else:
        form = RegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})


def user_management_required(view_func):
    """Decorator to check if user can manage other users"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.can_manage_users():
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('inventory_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@user_management_required
def user_management_view(request):
    """User management page for admins and managers"""
    # Get users based on role
    if request.user.is_admin():
        # Admins can see all users
        users = User.objects.all().order_by('-date_joined')
    else:
        # Managers can only see users they created and cashiers
        users = User.objects.filter(
            role='cashier'
        ).order_by('-date_joined')
    
    # Get reference codes
    if request.user.is_admin():
        reference_codes = ReferenceCode.objects.all()
    else:
        reference_codes = ReferenceCode.objects.filter(created_by=request.user)
    
    # Forms
    create_user_form = CreateUserForm(creator=request.user)
    generate_code_form = GenerateReferenceCodeForm(creator=request.user)
    
    context = {
        'users': users,
        'reference_codes': reference_codes,
        'create_user_form': create_user_form,
        'generate_code_form': generate_code_form,
    }
    
    return render(request, 'accounts/user_management.html', context)


@login_required
@user_management_required
def create_user_view(request):
    """Create a new user directly"""
    if request.method == 'POST':
        form = CreateUserForm(request.POST, creator=request.user)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User "{user.username}" created successfully as {user.get_role_display()}.')
            return redirect('user_management')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    
    return redirect('user_management')


@login_required
@user_management_required
def generate_reference_code_view(request):
    """Generate a new reference code"""
    if request.method == 'POST':
        form = GenerateReferenceCodeForm(request.POST, creator=request.user)
        if form.is_valid():
            ref_code = form.save()
            messages.success(request, f'Reference code "{ref_code.code}" generated successfully for {ref_code.get_role_for_display()} position.')
            return redirect('user_management')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    
    return redirect('user_management')


@login_required
@user_management_required
@require_POST
def delete_reference_code_view(request, code_id):
    """Delete a reference code"""
    ref_code = get_object_or_404(ReferenceCode, id=code_id)
    
    # Only allow deletion if code hasn't been used
    if ref_code.is_used:
        messages.error(request, 'Cannot delete a used reference code.')
        return redirect('user_management')
    
    # Only allow deletion by creator or admin
    if ref_code.created_by != request.user and not request.user.is_admin():
        messages.error(request, 'You do not have permission to delete this code.')
        return redirect('user_management')
    
    ref_code.delete()
    messages.success(request, 'Reference code deleted successfully.')
    return redirect('user_management')


@login_required
@user_management_required
@require_POST
def toggle_user_active_view(request, user_id):
    """Toggle user active status"""
    user = get_object_or_404(User, id=user_id)
    
    # Prevent self-deactivation
    if user == request.user:
        messages.error(request, 'You cannot deactivate your own account.')
        return redirect('user_management')
    
    # Managers can only toggle cashiers
    if not request.user.is_admin() and user.role != 'cashier':
        messages.error(request, 'You do not have permission to modify this user.')
        return redirect('user_management')
    
    user.is_active = not user.is_active
    user.save()
    
    status = 'activated' if user.is_active else 'deactivated'
    messages.success(request, f'User "{user.username}" has been {status}.')
    return redirect('user_management')
