from django.contrib import admin
from .models import Cart, CartLine

class CartLineInline(admin.TabularInline):
    model = CartLine
    extra = 1
    can_delete = True

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id' , 'user', 'created_at' , 'status')
    inlines = [CartLineInline]

@admin.register(CartLine)
class CartLineAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity' )
    search_fields = ('cart__user__username', 'product__name')
