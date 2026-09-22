from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

# 1. Custom form for ADDING a user
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('srn', 'email', 'role')

# 2. Custom form for EDITING a user
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('srn', 'email', 'role')

# 3. Apply these to the Admin panel
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    
    list_display = ('srn', 'email', 'role', 'is_staff')
    ordering = ('srn',)
    
    # Overriding fieldsets to remove 'username' completely
    fieldsets = (
        (None, {'fields': ('srn', 'email', 'password')}),
        ('Sports Information', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('srn', 'email', 'role', 'password1', 'password2'),
        }),
    )
    
    search_fields = ('srn', 'email')
    list_filter = ('role', 'is_staff', 'is_active')