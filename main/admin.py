from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('username', 'password', 'user_type')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type')


admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(CarrierCompany)
admin.site.register(ShipperCompany)
