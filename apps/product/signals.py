from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SizeGuide, SizeGuideItem, Product


@receiver(post_save, sender=SizeGuide)
def update_attributes(sender, instance, **kwargs):

	products = instance.product_set.all()

	print("Size Guide Updated")
	print(products)

        

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()