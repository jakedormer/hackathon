from apps.dashboard.models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# @receiver(post_save, sender=Profile)
# def create_auth_token(sender, instance, created, **kwargs):
		
# 	if instance.is_vendor == True:
# 		Token.objects.get_or_create(user=instance.user)