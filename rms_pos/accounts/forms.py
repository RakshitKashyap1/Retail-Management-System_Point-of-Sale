from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ReferenceCode


class RegistrationForm(UserCreationForm):
    """Form for new user registration with reference code validation"""
    reference_code = forms.CharField(
        max_length=12,
        help_text="Enter the reference code provided by your manager or admin.",
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter reference code',
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'reference_code']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add placeholders and classes to all fields
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Choose a username',
            'class': 'form-control'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Enter your email',
            'class': 'form-control'
        })
        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'Enter your first name',
            'class': 'form-control'
        })
        self.fields['last_name'].widget.attrs.update({
            'placeholder': 'Enter your last name',
            'class': 'form-control'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Create a password',
            'class': 'form-control'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm your password',
            'class': 'form-control'
        })
    
    def clean_reference_code(self):
        code = self.cleaned_data.get('reference_code', '').upper().strip()
        try:
            ref_code = ReferenceCode.objects.get(code=code)
            if not ref_code.is_valid():
                if ref_code.is_used:
                    raise forms.ValidationError("This reference code has already been used.")
                else:
                    raise forms.ValidationError("This reference code has expired.")
            return code
        except ReferenceCode.DoesNotExist:
            raise forms.ValidationError("Invalid reference code. Please contact your manager.")
    
    def save(self, commit=True):
        user = super().save(commit=False)
        code = self.cleaned_data.get('reference_code')
        ref_code = ReferenceCode.objects.get(code=code)
        
        # Set user role based on the reference code
        user.role = ref_code.role_for
        user.created_by = ref_code.created_by
        
        if commit:
            user.save()
            # Mark reference code as used
            ref_code.is_used = True
            ref_code.used_by = user
            ref_code.save()
        
        return user


class CreateUserForm(UserCreationForm):
    """Form for admin/manager to create new users directly"""
    role = forms.ChoiceField(
        choices=[('cashier', 'Cashier'), ('manager', 'Inventory Manager')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2']
    
    def __init__(self, *args, creator=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.creator = creator
        
        # Only admins can create managers
        if creator and not creator.is_admin():
            self.fields['role'].choices = [('cashier', 'Cashier')]
        
        # Add placeholders and classes
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Enter username',
            'class': 'form-control'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Enter email',
            'class': 'form-control'
        })
        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'First name',
            'class': 'form-control'
        })
        self.fields['last_name'].widget.attrs.update({
            'placeholder': 'Last name',
            'class': 'form-control'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Create password',
            'class': 'form-control'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm password',
            'class': 'form-control'
        })
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        if self.creator:
            user.created_by = self.creator
        if commit:
            user.save()
        return user


class GenerateReferenceCodeForm(forms.ModelForm):
    """Form to generate new reference codes"""
    class Meta:
        model = ReferenceCode
        fields = ['role_for']
        widgets = {
            'role_for': forms.Select(attrs={'class': 'form-control'})
        }
    
    def __init__(self, *args, creator=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.creator = creator
        
        # Only admins can generate codes for managers
        if creator and not creator.is_admin():
            self.fields['role_for'].choices = [('cashier', 'Cashier')]
    
    def save(self, commit=True):
        ref_code = super().save(commit=False)
        if self.creator:
            ref_code.created_by = self.creator
        if commit:
            ref_code.save()
        return ref_code
