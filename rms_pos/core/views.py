from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    if request.user.is_admin() or request.user.is_manager():
        return redirect('inventory_dashboard')
    elif request.user.is_cashier():
        return redirect('pos_dashboard')
    return render(request, 'base.html') # Fallback
