from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . models import User
# Register your models here.
class UserAdmin(UserAdmin):
    list_display = ('email', 'is_institution_admin', 'is_superuser', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)
    readonly_fields = ('date_joined', 'last_login',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        # ('Personal Info', {'fields': ('cert_no', 'pic')}),
        ('Permissions', {'fields': (
            'is_institution_admin', 'is_staff', 'is_superuser', 'is_active')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

admin.site.register(User, UserAdmin)