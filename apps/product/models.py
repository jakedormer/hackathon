from django.db import models
from django.template.defaultfilters import slugify
from apps.dashboard.models import Vendor
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.


class Category(models.Model):


	name = models.CharField(max_length=30, unique=True)
	slug = models.SlugField(unique=True, null=True)
	description = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.name.title()
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)

class AttributeOptionGroup(models.Model):
	"""
	Defines a group of options that collectively may be used as an
	attribute type

	For example, Language
	"""
	name = models.CharField(max_length=128)

	def __str__(self):
		return self.name

	@property
	def option_summary(self):
		options = [o.option for o in self.options.all()]
		return ", ".join(options)

class Attribute(models.Model):

	name = models.CharField(max_length=128, null=False, unique=True)
	
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

	option_group = models.ForeignKey(
		AttributeOptionGroup,
		blank=True,
		null=True,
		on_delete=models.CASCADE,
		verbose_name="Option Group",
		help_text='Select an option group if using type "Option" or "Multi Option"'
		)

	size_guide_info = models.TextField(max_length=250, null=True, blank=True)


	def __str__(self):
		return self.name




class AttributeOption(models.Model):
	"""
	Provides an option within an option group for an attribute type
	Examples: In a Language group, English, Greek, French
	"""
	group = models.ForeignKey(
		AttributeOptionGroup,
		on_delete=models.CASCADE,
		related_name='options',
		)
	option = models.CharField(max_length=255)

	order = models.PositiveIntegerField(null=True, blank=True, help_text="Used to order sizing in the store, 1 is the smallest")

	def __str__(self):
		return self.option




class CategoryAttributeGroup(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
	attribute = models.ManyToManyField(Attribute)

	def __str__(self):
		return self.category.name.title()

	def get_attributes(self):
		return ", ".join([a.name for a in self.attribute.all()])


class Size(models.Model):

	name = models.CharField(max_length=50)
	order = models.PositiveIntegerField(null=False, help_text="Used to order the sizes, 1 is the smallest")

	def __str__(self):
		return self.name

class SizeGuide(models.Model):

	name 			= models.CharField(max_length=100, null=False, blank=False, unique=True)
	vendor 			= models.ForeignKey(Vendor, on_delete=models.CASCADE)
	category		= models.ForeignKey(Category, on_delete=models.CASCADE)

	class Meta:
		unique_together = ('name', 'vendor')

	def __str__(self):
		return self.name

class SizeGuideItem(models.Model):

	size_guide		= models.ForeignKey(SizeGuide, on_delete=models.CASCADE)
	size 			= models.ForeignKey(Size, on_delete=models.CASCADE)
	attribute  		= models.ForeignKey(Attribute, on_delete=models.CASCADE)
	value     		= models.FloatField(null=False)

	class Meta:
		unique_together = ('size_guide', 'size', 'attribute')



class Product(models.Model):

	external_id = models.CharField(max_length=100, null=False, blank=False)
	title = models.CharField(max_length=128, blank=True)
	description = models.TextField(null=True, blank=True)
	slug = models.SlugField(null=True, blank=True)
	vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True)


	#: Type of product, e.g. T-Shirt, Book, etc.
	#: None for variants, they inherit their parent's product class

	category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.PROTECT)

	STANDALONE, PARENT, VARIANT = 'standalone', 'parent', 'variant'
	PRODUCT_TYPE_CHOICES = [
		('standalone', 'Stand-alone product'),
		('parent', 'Parent product'),
		('variant', 'Variant product')
	]
	product_type = models.CharField(max_length=10, choices=PRODUCT_TYPE_CHOICES)


	parent = models.ForeignKey(
		'self',
		blank=True,
		null=True,
		on_delete=models.CASCADE,
		related_name='children',
		verbose_name= "Parent product",
		help_text= ("Only choose a parent product if you're creating a variant "
					"variant.  For example if this is a size "
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

	image_src = models.URLField(null=True)
	size_guide = models.ForeignKey(SizeGuide, null=True, blank=True, on_delete=models.SET_NULL)
	attributes = models.ManyToManyField(
			'product.Attribute',
			through='AttributeValue',
			verbose_name= "Attributes",
			help_text= "A product attribute is something that this product may "
						"have, such as a size, as specified by its class")

	external_url = models.URLField(max_length=200, null=True, blank=True)

	date_modified = models.DateTimeField(auto_now=True)

	description = models.TextField(null=True, blank=True)

	published = models.BooleanField(default=False)

	def clean(self):
		"""
		Validate a product. Those are the rules:

		+---------------+-------------+--------------+--------------+
		|               | stand alone | parent       | variant      |
		+---------------+-------------+--------------+--------------+
		| title         | required    | required     | optional     |
		+---------------+-------------+--------------+--------------+
		| product class | required    | required     | must be None |
		+---------------+-------------+--------------+--------------+
		| parent        | forbidden   | forbidden    | required     |
		+---------------+-------------+--------------+--------------+
		| stockrecords  | 0 or more   | forbidden    | 0 or more    |
		+---------------+-------------+--------------+--------------+
		| categories    | 1 or more   | 1 or more    | forbidden    |
		+---------------+-------------+--------------+--------------+
		| attributes    | optional    | optional     | optional     |
		+---------------+-------------+--------------+--------------+
		| options       | optional    | optional     | forbidden    |
		+---------------+-------------+--------------+--------------+

		Because the validation logic is quite complex, validation is delegated
		to the sub method appropriate for the product's product_type.
		"""

		if self.product_type:
			getattr(self, '_clean_%s' % self.product_type)()

	def _clean_standalone(self):
		"""
		Validates a stand-alone product
		"""
		if not self.title:
			raise ValidationError(("Your product must have a title."))
		if not self.category:
			raise ValidationError(("Your product must have a category."))
		if self.parent:
			raise ValidationError(("Only variant products can have a parent."))
		if not self.vendor:
			raise ValidationError(("Your product must have vendor"))
		if not self.size:
			raise ValidationError(("Your product must have a size"))

	def _clean_variant(self):
		"""
		Validates a variant product
		"""
		if not self.parent:
			raise ValidationError(("A variant product needs a parent."))
		# if not self.size:
		# 	raise ValidationError(("A variant product needs a size"))
		if self.parent and not self.parent.is_parent:
			raise ValidationError(
				("You can only assign variant products to parent products."))

		if self.parent and self.vendor != self.parent.vendor:
			raise ValidationError(
				("A variant product must have the same vendor as its parent product."))
		# if not self.size:
		# 	raise ValidationError(("Your product must have a size"))

		# Note that we only forbid options on product level


	def _clean_parent(self):
		"""
		Validates a parent product.

		"""

		if not self.title:
			raise ValidationError(("Your product must have a title."))
		if not self.category:
			raise ValidationError(("Your product must have a category."))
		if self.parent:
			raise ValidationError(("Only variant products can have a parent."))
		if not self.vendor:
			raise ValidationError(("Your product must have vendor"))
		if self.size:
			raise ValidationError(("Parent products can not have a size."))
		# if self.attributes.count() > 0:
		# 	raise ValidationError(
		# 		("A parent product can not have attributes"))

	def get_product_category(self):
		"""
		Return a product's item class. Variant products inherit their parent's.
		"""
		if self.is_variant:
			return self.parent.category
		else:
			return self.category


	# Properties

	@property
	def is_standalone(self):
		return self.product_type == self.STANDALONE

	@property
	def is_parent(self):
		return self.product_type == self.PARENT

	@property
	def is_variant(self):
		return self.product_type == self.VARIANT

	@property
	def size(self):
		try:
			return self.attribute_values.filter(attribute__name="size").first().value_option

		except AttributeError:

			pass

	@property
	def num_in_stock(self):
		try:
			num_in_stock = self.stockrecords.first().num_in_stock
		except ObjectDoesNotExist:
			num_in_stock = 0

		return num_in_stock
	

	@property
	def price(self):
		if self.product_type == "parent":
			try:
				price = self.children.first().stockrecords.first().price_inc_tax

			except AttributeError:
				price = None

		elif self.product_type == "standalone":
			try:
				price = self.stockrecords.first().price_inc_tax

			except AttributeError:
				price = None

		return price

	@property
	def total_in_stock(self):
		if self.is_parent:
			quantity = 0
			for x in self.children.all():
				for y in x.stockrecords.all():
					quantity += y.num_in_stock
		else:
			quantity = self.num_in_stock

		return quantity


	


	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if self.is_variant:
			self.slug = self.parent.slug
			# self.title = self.parent.title + " - " + self.attribute_values.filter(attribute__name="size").first().value_text
			self.title = self.parent.title
			self.category = self.parent.category
			self.vendor = self.parent.vendor
			self.external_url = self.parent.external_url
			self.image_src = self.parent.image_src
		# if self.is_parent:

		if self.is_parent or self.is_standalone:
			self.slug = slugify(self.title)
			
		super(Product, self).save(*args, **kwargs)




class AttributeValue(models.Model):

	attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, verbose_name= "Attribute")
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attribute_values', verbose_name="Product")

	value_text = models.CharField('Text', max_length=100, blank=True, null=True)
	value_float = models.FloatField('Float', blank=True, null=True, db_index=True)
	value_option = models.ForeignKey(AttributeOption, blank=True, null=True, on_delete=models.CASCADE)

	class Meta:
		unique_together = ('attribute', 'product')


	@property
	def value(self):
		'Returns the value of the attribute, from value_text, value_float, value_option'
		if self.value_text:
			return self._value

		if self.value_float:
			return self.value_float
			
		if self.value_option:
			return self.value_option

	def __str__(self):
		return self.product.title + ' - ' + self.attribute.name



