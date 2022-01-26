from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email', 'username', 'first_name', 'organization', 'position')
    list_filter = ('email', 'username', 'first_name', 'is_active', 'is_staff', 'organization', 'position')
    ordering = ('-start_date', )
    list_display = ('email', 'username', 'first_name',
                    'is_active', 'is_staff', 'organization', 'position')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'first_name', 'organization', 'position')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'password1', 'password2', 'is_active', 'is_staff',  'organization', 'position')
        }),
    )


admin.site.register(User, UserAdminConfig)
