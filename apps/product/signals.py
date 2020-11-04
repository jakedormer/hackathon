from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SizeGuide, SizeGuideItem, Product, AttributeValue, Attribute


# @receiver(post_save, sender=SizeGuide)
# def update_attributes(sender, instance, **kwargs):

# 	products = instance.product_set.all()

# 	print("Size Guide Updated")
# 	print(products)

# Create/ update brand attribute where names is equal to the name of vendor
@receiver(post_save, sender=Product)
def product_signal(sender, instance, **kwargs):

	AttributeValue.objects.update_or_create(
		product=instance, 
		attribute=Attribute.objects.get(name="brand"),
		defaults={
			'value_text': instance.vendor.name
			}
		)

	if instance.is_parent:

		for variant in instance.children.all():

			variant.title = instance.title
			variant.slug = instance.slug
			variant.category = instance.category
			variant.image_src = instance.image_src
			variant.size_guide = instance.size_guide
			variant.external_url = instance.external_url

			variant.save()




# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()