from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.db import models

# Register your models here.

from .models import *

class AttributeValueAdmin(admin.TabularInline):
    model = AttributeValue
    extra = 0

class ProductAdmin(admin.ModelAdmin):

	list_display = ('vendor', 'get_product_category', 'title', 'product_type', 'date_created')
	list_filter = ('vendor', 'category', 'product_type')
	inlines = (AttributeValueAdmin,)
	ordering = ('vendor', 'title', 'product_type')

class AttributeAdmin(admin.ModelAdmin):
	list_display = ('name', 'type')



class AttributeGroupAdmin(admin.ModelAdmin):
	formfield_overrides = {
	        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
	    }

	list_display = ('category', 'get_attributes')

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(AttributeGroup, AttributeGroupAdmin)
admin.site.register(AttributeValue)


