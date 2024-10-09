from django.contrib import admin
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'total_amount', 'created_at')
    search_fields = ('order_number', 'user__username')
    list_filter = ('status', 'created_at')
    readonly_fields = ('created_at', 'total_amount')

    def save_model(self, request, obj, form, change):
        if not obj.total_amount:
            obj.total_amount = obj.calculate_total()
        super().save_model(request, obj, form, change)

admin.site.register(Order, OrderAdmin)
