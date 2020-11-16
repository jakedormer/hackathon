from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.


class CartItemInline(admin.TabularInline):
    model = CartItem


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity')


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'session_key', 'status', 'num_lines', 'num_items', 'date_created', 'date_modified', 'date_submitted',)
    readonly_fields = ('date_created', 'date_merged', 'date_submitted')
    inlines = [CartItemInline]


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
