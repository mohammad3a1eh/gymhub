from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'phone_number', 'gender', 'age', 'is_verified')
    fieldsets = UserAdmin.fieldsets + (
        ('اطلاعات اضافی', {
            'fields': ('phone_number', 'gender', 'age', 'height', 'weight', 'is_verified'),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('اطلاعات اضافی', {
            'fields': ('phone_number', 'gender', 'age', 'height', 'weight', 'is_verified'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
