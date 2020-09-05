from django.contrib import admin

# Register your models here.
from .models import Vendor, Profile, Platform, APICredential

admin.site.register(Profile)
admin.site.register(Platform)

class APICredentialAdmin(admin.TabularInline):
    model = APICredential
    extra = 0

class VendorAdmin(admin.ModelAdmin):
	inlines = (APICredentialAdmin, )


admin.site.register(Vendor, VendorAdmin)