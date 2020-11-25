from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class Platform(models.Model):


	name = models.CharField(max_length=30, null=True, unique=True)
	storefront_endpoint = models.CharField(max_length=200, null=True, blank=True)
	sales_channel_endpoint = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		# return self.get_name_display()
		return self.name


class Vendor(models.Model):

	name = 				models.CharField(max_length=30, unique=True, help_text="The store name within the shopify url")
	display_name = 		models.CharField(max_length=30)
	platform = 			models.OneToOneField(Platform, on_delete=models.PROTECT, null=True, blank=True)
	api_access_token = 	models.CharField(max_length=200, null=True, blank=True)
	enabled = 			models.BooleanField(default=False)
	commission = 		models.DecimalField(max_digits=10, decimal_places=4, null=True, help_text="The vendor commission rate, set it as a decimal e.g. 15% = 0.15")
	free_shipping = 	models.DecimalField(max_digits=10, decimal_places=4, null=True, help_text="The vendors current free shipping threshold")
	instagram = 		models.CharField(max_length=100, null=True, blank=True)

	def __str__(self):
		return self.display_name

	@property
	def num_items(self):
		return len(self.product_set.all())

	@property
	def num_items_published(self):
		return len(self.product_set.filter(published=True))
	

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, null=True, blank=True)
	is_vendor = models.BooleanField(null=True)
	email_pref = models.BooleanField(default=False)
	sms_pref = models.BooleanField(default=False)
	favourites = models.ManyToManyField(Vendor, related_name="favourites", blank=True)


	# Create a profile object when a user is created and create api_token
	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)
			instance.email = instance.username
			instance.save()

		# Create token if user is a vendor
		if instance.profile.is_vendor == True:
			
			Token.objects.get_or_create(user=instance)

			

	def __str__(self):
		return self.user.first_name

 



