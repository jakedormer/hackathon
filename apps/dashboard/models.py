from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Platform(models.Model):


	name = models.CharField(max_length=30, null=True, unique=True)

	def __str__(self):
		# return self.get_name_display()
		return self.name


class Vendor(models.Model):

	name = models.CharField(max_length=30, unique=True)
	platform = models.ManyToManyField(Platform, through="APICredential")

	def __str__(self):
		return self.name.title()

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, null=True, blank=True)
	is_vendor = models.BooleanField()

	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)

	@receiver(post_save, sender=User)
	def save_user_profile(sender, instance, **kwargs):
		instance.profile.save()

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
 



