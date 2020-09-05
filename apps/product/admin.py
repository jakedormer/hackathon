from django.contrib import admin

# Register your models here.

from .models import Product, Category, Attribute

class ProductAdmin(admin.ModelAdmin):

	list_display = ('vendor', 'category', 'title', 'product_type')
	list_filter = ('vendor', 'category', 'product_type')

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Attribute)