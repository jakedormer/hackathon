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

	name = models.CharField(max_length=30, unique=True, help_text="The store name within the shopify url")
	display_name = models.CharField(max_length=30)
	platform = models.ManyToManyField(Platform, through="APICredential")
	enabled = models.BooleanField(default=False)
	commission = models.DecimalField(max_digits=10, decimal_places=4, help_text="The vendor commission rate, set it as a decimal e.g. 15% = 0.15")

	def __str__(self):
		return self.name

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

class APICredential(models.Model):

	vendor 						= models.ForeignKey(Vendor, on_delete=models.CASCADE)
	platform 					= models.ForeignKey(Platform, on_delete=models.CASCADE)
	nonce						= models.CharField(max_length=200, null=True, blank=True)
	access_token 				= models.CharField(max_length=200, null=True, blank=True)
	storefront_access_token 	= models.CharField(max_length=200, null=True, blank=True)
	categories 					= models.CharField(max_length=500, null=True, blank=True)
	scopes	 					= models.CharField(max_length=500, null=True, blank=True)
	date_modified 				= models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.vendor.name.title() + "-" + self.platform.name.title()


	class Meta:
		unique_together = ('vendor', 'platform')
 



