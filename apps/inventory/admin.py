from django.contrib import admin
from .models import *

class StockRecordAdmin(admin.ModelAdmin):

	list_display = ('product_id', 'product', 'get_product_type', 'price_inc_tax', 'num_in_stock')

	def get_product_type(self, obj):
	        return obj.product.product_type.title()

	get_product_type.admin_order_field  = 'Product Type'  #Allows column order sorting
	get_product_type.short_description = 'Product Type'

admin.site.register(StockRecord, StockRecordAdmin)

