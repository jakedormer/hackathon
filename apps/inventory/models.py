from django.db import models
from apps.product.models import Product

class StockRecord(models.Model):

	"""
	A stock record.

	This records information about a product from a fulfilment partner, such as
	their SKU, the number they have in stock and price information.

	Stockrecords are used by 'strategies' to determine availability and pricing
	information for the customer.
	"""

	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stockrecords", verbose_name="Product")

	# Price including tax
	price_inc_tax = models.DecimalField("Price (incl. tax)", decimal_places=2, max_digits=12, blank=True, null=True)

	#: Number of items in stock
	num_in_stock = models.PositiveIntegerField("Number in stock", blank=True, null=True)