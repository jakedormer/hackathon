from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.db import models

# Register your models here.

from .models import *

class AttributeOptionInline(admin.TabularInline):
    model = AttributeOption

class AttributeOptionGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'option_summary')
    inlines = [AttributeOptionInline, ]

class AttributeValueAdmin(admin.TabularInline):
    model = AttributeValue
    extra = 0

class ProductAdmin(admin.ModelAdmin):

	list_display = ('id', 'external_id', 'attr_count', 'vendor', 'get_product_category', 'title', 'size', 'product_type', 'date_created')
	list_filter = ('vendor', 'category', 'product_type')
	inlines = (AttributeValueAdmin,)
	ordering = ('vendor', 'title', '-product_type')

	def attr_count(self, x):
			
			return x.attributes.count()



class AttributeAdmin(admin.ModelAdmin):
	list_display = ('name', 'type')

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('id', 'name',)

class AttributeGroupAdmin(admin.ModelAdmin):
	formfield_overrides = {
	        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
	    }

	list_display = ('category', 'get_attributes')

class SizeGuideInline(admin.TabularInline):
	model = SizeGuideItem


class SizeGuideAdmin(admin.ModelAdmin):
	list_display = ('name', 'vendor', 'category')
	inlines = [SizeGuideInline, ]

class SizeAdmin(admin.ModelAdmin):
	list_display = ('name', 'order',)

admin.site.register(AttributeOptionGroup, AttributeOptionGroupAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(CategoryAttributeGroup, AttributeGroupAdmin)
admin.site.register(AttributeValue)
admin.site.register(Size, SizeAdmin)
admin.site.register(SizeGuide, SizeGuideAdmin)




