from django.db import models
from django.template.defaultfilters import slugify
from apps.dashboard.models import Vendor
from django.core.exceptions import ValidationError

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

class Size(models.Model):

	value = models.CharField(max_length=50)
	order = models.PositiveIntegerField(null=False, help_text="Used to order the sizes, 1 is the smallest")

	def __str__(self):
		return self.value

class Product(models.Model):

	id = models.CharField(max_length=100, null=False, blank=False, primary_key=True)
	title = models.CharField(max_length=128, blank=True)
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

	image_src = models.URLField(null=True)
	size = models.ForeignKey(Size, blank=True, null=True, on_delete=models.SET_NULL)
	attributes = models.ManyToManyField(
	        'product.Attribute',
	        through='AttributeValue',
	        verbose_name= "Attributes",
	        help_text= "A product attribute is something that this product may "
	                    "have, such as a size, as specified by its class")

	external_url = models.URLField(max_length=200, null=True, blank=True)

	date_modified = models.DateTimeField(auto_now=True)

	def clean(self):
	    """
	    Validate a product. Those are the rules:

	    +---------------+-------------+--------------+--------------+
	    |               | stand alone | parent       | child        |
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
	        raise ValidationError(("Only child products can have a parent."))
	    if not self.vendor:
	        raise ValidationError(("Your product must have vendor"))
	    if not self.size:
	    	raise ValidationError(("Your product must have a size"))

	def _clean_child(self):
	    """
	    Validates a child product
	    """
	    if not self.parent:
	        raise ValidationError(("A child product needs a parent."))
	    if not self.size:
	        raise ValidationError(("A child product needs a size"))
	    if self.parent and not self.parent.is_parent:
	        raise ValidationError(
	            ("You can only assign child products to parent products."))
	    if self.category:
	        raise ValidationError(
	            ("A child product can't have a product class."))
	    if self.slug:
	        raise ValidationError(
	            ("A child product can't have a url slug."))
	    if self.parent and self.vendor != self.parent.vendor:
	        raise ValidationError(
	            ("A child product must have the same vendor as its parent product."))
	    if not self.size:
	    	raise ValidationError(("Your product must have a size"))

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
	        raise ValidationError(("Only child products can have a parent."))
	    if not self.vendor:
	        raise ValidationError(("Your product must have vendor"))
	    if self.size:
	    	raise ValidationError(("Parent products can not have a size."))
	    if self.attributes.count() > 0:
	        raise ValidationError(
	            ("A parent product can not have attributes"))

	def get_product_category(self):
		"""
		Return a product's item class. Child products inherit their parent's.
		"""
		if self.is_child:
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
	def is_child(self):
		return self.product_type == self.CHILD


	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if self.is_child:
			self.slug = None
			self.title = self.parent.title + " - " + self.size.value
			self.vendor = self.parent.vendor
			self.external_url = self.parent.external_url
			self.image_src = self.parent.image_src
		# if self.is_parent:

		# 	self.attributes = None
		# 	self.slug = slugify(self.title) + "-" + str(self.id)
			
		super(Product, self).save(*args, **kwargs)


# class AttributeGroup(models.Model):

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

    def __str__(self):
        return self.option


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

	def __str__(self):
		return self.name


class CategoryAttributeGroup(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
	attribute = models.ManyToManyField(Attribute)

	def __str__(self):
		return self.category.name.title()

	def get_attributes(self):
	    return ", ".join([a.name for a in self.attribute.all()])


class AttributeValue(models.Model):

    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, verbose_name= "Attribute")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attribute_values', verbose_name="Product")

    value_text = models.CharField('Text', max_length=100, blank=True, null=True)
    value_float = models.FloatField('Float', blank=True, null=True, db_index=True)
    value_option = models.ForeignKey(AttributeOption, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('attribute', 'product')


class SizeGuide(models.Model):

	name 			= models.CharField(max_length=100, null=False, blank=False, unique=True)
	vendor 			= models.ForeignKey(Vendor, on_delete=models.CASCADE)
	category		= models.ForeignKey(Category, on_delete=models.CASCADE)

	class Meta:
		unique_together = ('name', 'vendor')

class SizeGuideItem(models.Model):

	size_guide		= models.ForeignKey(SizeGuide, on_delete=models.CASCADE)
	size 			= models.ManyToManyField(Size)
	attribute  		= models.ManyToManyField(Attribute)
	value     		= models.FloatField(null=False)


