from django.db import models
from django.template.defaultfilters import slugify
from apps.dashboard.models import Vendor
from django.core.exceptions import ValidationError

# Create your models here.


class Category(models.Model):

	CATEGORY_CHOICES = [
		('t-shirts', 'T-Shirts'),
		('shirts', 'Shirts'),
	]

	name = models.CharField(max_length=30, choices=CATEGORY_CHOICES, unique=True)
	slug = models.SlugField(unique=True, null=True)
	description = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.name
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)


class Product(models.Model):

	title = models.CharField(max_length=128, blank=True, unique=True)
	description = models.TextField(null=True, blank=True)
	slug = models.SlugField(null=True, unique=True, blank=True)
	vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True)


	#: Type of product, e.g. T-Shirt, Book, etc.
	#: None for child products, they inherit their parent's product class

	category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.PROTECT)

	STANDALONE, PARENT, CHILD = 'standalone', 'parent', 'child'
	PRODUCT_TYPE_CHOICES = [
		('standalone', 'Stand-alone product'),
		('parent', 'Parent product'),
		('child', 'Child product')
	]
	product_type = models.CharField(max_length=10, choices=PRODUCT_TYPE_CHOICES)


	parent = models.ForeignKey(
		'self',
		blank=True,
		null=True,
		on_delete=models.CASCADE,
		related_name='children',
		verbose_name= "Parent product",
		help_text= ("Only choose a parent product if you're creating a child "
					"product.  For example if this is a size "
					"4 of a particular t-shirt.  Leave blank if this is a "
					"stand-alone product (i.e. there is only one version of"
					" this product).")
		)

	date_created = models.DateTimeField(("Date created"), auto_now_add=True, db_index=True)

	is_discountable = models.BooleanField(
		("Is discountable?"), default=True, help_text= (
			"This flag indicates if this product can be used in an offer "
			"or not")
		)
	#Images

	image_src = models.URLField(null=True)

	# def _clean_standalone(self):
	#     """
	#     Validates a stand-alone product
	#     """
	#     if not self.title:
	#         raise ValidationError(_("Your product must have a title."))
	#     if not self.product_class:
	#         raise ValidationError(_("Your product must have a product class."))
	#     if self.parent_id:
	#         raise ValidationError(_("Only child products can have a parent."))

	def _clean_child(self):
	    """
	    Validates a child product
	    """
	    if not self.parent_id:
	        raise ValidationError(_("A child product needs a parent."))
	    if self.parent_id and not self.parent.is_parent:
	        raise ValidationError(
	            _("You can only assign child products to parent products."))
	    if self.product_class:
	        raise ValidationError(
	            _("A child product can't have a product class."))
	    if self.pk and self.categories.exists():
	        raise ValidationError(
	            _("A child product can't have a category assigned."))
	    # Note that we only forbid options on product level
	    if self.pk and self.product_options.exists():
	        raise ValidationError(
	            _("A child product can't have options."))

	def __str__(self):
		return self.title

	# def save(self, *args, **kwargs):
	# 	if self.product_type == "parent" or self.product_type == "standalone":
	# 		self.slug = slugify(self.title)
	# 		super(Product, self).save(*args, **kwargs)

# class AttributeGroup(models.Model):




class Attribute(models.Model):

	name = models.CharField(max_length=128)
	

	#Attribute Choices
	TEXT = "text"
	INTEGER = "integer"
	BOOLEAN = "boolean"
	FLOAT = "float"
	RICHTEXT = "richtext"
	DATE = "date"
	DATETIME = "datetime"
	OPTION = "option"
	MULTI_OPTION = "multi_option"
	ENTITY = "entity"
	FILE = "file"
	IMAGE = "image"
	TYPE_CHOICES = (
		(TEXT, ("Text")),
		(INTEGER, ("Integer")),
		(BOOLEAN, ("True / False")),
		(FLOAT, ("Float")),
		(RICHTEXT, ("Rich Text")),
		(DATE, ("Date")),
		(DATETIME, ("Datetime")),
		(OPTION, ("Option")),
		(MULTI_OPTION, ("Multi Option")),
		(ENTITY, ("Entity")),
		(FILE, ("File")),
		(IMAGE, ("Image")),
	)

	type = models.CharField(
		choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0],
		max_length=20, verbose_name="Type")

	def __str__(self):
		return self.name




