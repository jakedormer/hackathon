from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from .models import CartItem


@receiver(post_delete, sender=CartItem)
def product_signal(sender, instance, **kwargs):

	try:

		if instance.cart.num_lines == 0:

			instance.cart.delete()

	except ObjectDoesNotExist:

		pass
