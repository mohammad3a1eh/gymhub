from django.contrib import admin
from .models import PurchaseRequest

class PurchaseRequestAdmin(admin.ModelAdmin):
    list_display = ('id' ,'user', 'sport_type', 'created_at', 'is_approved', 'is_paid', 'price',
                   'get_first_name', 'get_last_name', 'get_age', 'get_height', 'get_weight')
    
    search_fields = ('user__first_name', 'user__last_name', 'sport_type')
    list_filter = ('sport_type', 'is_approved', 'is_paid', 'created_at')
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('program_file' ,'user', 'sport_type', 'goals', 'price')
        }),
        ('وضعیت', {
            'fields': ('is_approved', 'is_paid')
        }),
        ('اطلاعات کاربر', {
            'fields': ('get_age', 'get_height', 'get_weight', 'get_gender'),
            'description': 'این اطلاعات از پروفایل کاربر خوانده می‌شود'
        })
    )
    
    readonly_fields = ('get_age', 'get_height', 'get_weight', 'get_gender')
    
    def get_gender(self, obj):
        return obj.user.gender
    get_gender.short_description = 'جنسیت'
    
    # Methods to access user fields
    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'
    
    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Last Name'
    
    def get_age(self, obj):
        return obj.user.age
    get_age.short_description = 'Age'
    
    def get_height(self, obj):
        return obj.user.height
    get_height.short_description = 'Height'
    
    def get_weight(self, obj):
        return obj.user.weight
    get_weight.short_description = 'Weight'

admin.site.register(PurchaseRequest, PurchaseRequestAdmin)
