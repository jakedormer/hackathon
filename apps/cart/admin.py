from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.


class CartItemInline(admin.TabularInline):
    model = CartItem


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity')


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'session_key', 'status', 'num_lines', 'date_created', 'date_submitted',)
    readonly_fields = ('owner', 'date_merged', 'date_submitted')
    inlines = [CartItemInline]


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
