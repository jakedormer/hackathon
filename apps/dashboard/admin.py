from django.contrib import admin

# Register your models here.
from .models import Vendor, Profile, Platform, APICredential


admin.site.register(Platform)

class APICredentialAdmin(admin.TabularInline):
	model = APICredential
	extra = 0

class VendorAdmin(admin.ModelAdmin):
	inlines = (APICredentialAdmin, )
	list_display = ('id', 'name', 'display_name', 'commission')

class ProfileAdmin(admin.ModelAdmin):

	list_display = ('profile_username','vendor', 'email_pref', 'sms_pref')
	filter_horizontal = ('favourites',)

	def profile_username(self, x):
		
		return x.user.username

	# def get_favourites(self, x):

	# 	return " ".join(x for y in x.favourites)


admin.site.register(Vendor, VendorAdmin)
admin.site.register(Profile, ProfileAdmin)