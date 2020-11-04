from django.db import models
from django.contrib.auth.models import User
from apps.product.models import Product
from django.core.exceptions import ValidationError

# Create your models here.

class Cart(models.Model):

	owner = owner = models.ForeignKey(
		User,
		null=True,
		related_name='baskets',
		on_delete=models.CASCADE,
		)

	session_key = models.CharField(max_length=100, null=True, blank=True)

	OPEN, MERGED, SAVED, FROZEN, SUBMITTED = (
		"Open", "Merged", "Saved", "Frozen", "Submitted")
	
	STATUS_CHOICES = (
		(OPEN, ("Open - currently active")),
		(MERGED, ("Merged - superceded by another basket")),
		(SAVED, ("Saved - for items to be purchased later")),
		(FROZEN, ("Frozen - the basket cannot be modified")),
		(SUBMITTED, ("Submitted - has been ordered at the checkout")),
	)

	status = models.CharField(max_length=128, default=OPEN, choices=STATUS_CHOICES)

	date_created = models.DateTimeField(auto_now_add=True)
	date_merged = models.DateTimeField(null=True, blank=True)
	date_submitted = models.DateTimeField(null=True, blank=True)

	# ==========
	# Properties
	# ==========

	@property
	def num_lines(self):
		"""Return number of lines"""
		return self.cartitem_set.all().count()

	@property
	def num_items(self):
		"""Return number of items"""
		return sum(line.quantity for line in self.cartitem_set.all())


	def __str__(self):

		return (
			"%(status)s basket (owner: %(owner)s, lines: %(num_lines)d)") \
			% {'status': self.status,
			   'owner': self.owner,
			   'num_lines': self.num_lines
			   }

	def clean(self):

		return

class CartItem(models.Model):

	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

	# line_reference = SlugField(max_length=128, db_index=True)

	product = models.ForeignKey(Product ,on_delete=models.CASCADE)

	quantity = models.PositiveIntegerField(default=1)

	class Meta:
		ordering = ['product__vendor']

	@property
	def sub_total(self):
		"""Return sub total"""
		return self.quantity * self.product.stockrecords.first().price_inc_tax

	def clean(self):

		if self.product.product_type == 'parent':
			raise ValidationError("A parent product cannot be in a cart item")


			



