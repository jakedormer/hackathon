from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.db import models
from django.utils.translation import ngettext
from django.contrib import messages


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

	list_display = ('id', 'published', 'external_id', 'attr_count', 'vendor', 'get_product_category', 'title', 'get_size', 'product_type', 'date_created')
	list_filter = ('vendor', 'category', 'product_type')
	inlines = (AttributeValueAdmin,)
	ordering = ('vendor', 'title', '-product_type')
	actions = ["publish"]

	def attr_count(self, x):
			
		return x.attributes.count()

	def get_size(self, x):
		
		try:

			return x.attribute_values.filter(attribute__name="size").first().value_option

		except:

			return None

	def publish(self, request, queryset):

		updated = queryset.update(published=True)
		self.message_user(request, ngettext(
            '%d product was successfully marked as published.',
            '%d products were successfully marked as published.',
            updated,
        ) % updated, messages.SUCCESS)



class AttributeAdmin(admin.ModelAdmin):
	list_display = ('name', 'type', )

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




