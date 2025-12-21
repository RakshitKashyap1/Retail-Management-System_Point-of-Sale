from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Inventory Manager'),
        ('cashier', 'Cashier'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='cashier')
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_users')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def is_admin(self):
        return self.role == 'admin'

    def is_manager(self):
        return self.role == 'manager'

    def is_cashier(self):
        return self.role == 'cashier'
    
    def can_manage_users(self):
        """Check if user can create/manage other users"""
        return self.role in ('admin', 'manager')


class ReferenceCode(models.Model):
    """Reference codes that managers/admins generate for new employee registration"""
    ROLE_CHOICES = (
        ('manager', 'Inventory Manager'),
        ('cashier', 'Cashier'),
    )
    
    code = models.CharField(max_length=12, unique=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generated_codes')
    role_for = models.CharField(max_length=20, choices=ROLE_CHOICES, default='cashier')
    is_used = models.BooleanField(default=False)
    used_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='used_code')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        if not self.code:
            # Generate a unique 8-character code
            self.code = uuid.uuid4().hex[:8].upper()
        if not self.expires_at:
            # Default expiry: 7 days
            self.expires_at = timezone.now() + timezone.timedelta(days=7)
        super().save(*args, **kwargs)
    
    def is_valid(self):
        """Check if code is still valid (not used and not expired)"""
        return not self.is_used and timezone.now() < self.expires_at
    
    def __str__(self):
        return f"{self.code} - {self.get_role_for_display()} (by {self.created_by.username})"
    
    class Meta:
        ordering = ['-created_at']
