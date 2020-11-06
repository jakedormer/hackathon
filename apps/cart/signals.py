from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import CartItem


@receiver(post_delete, sender=CartItem)
def product_signal(sender, instance, **kwargs):

	if instance.cart.num_lines == 0:

		instance.cart.delete()