from django.contrib.auth.models import User
from apps.dashboard.models import APICredential
from rest_framework import serializers
from apps.dashboard.models import Vendor, Platform

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class APICredentialSerializer(serializers.Serializer):

    vendor__name = serializers.CharField(max_length=100,)
    platform__name = serializers.CharField(max_length=100)
    access_token = serializers.CharField(max_length=100)

    # vendor = VendorSerializer(many=True, read_only=True)
    # platform = PlatformSerializer(many=True, read_only=True)
    # access_token = serializers.CharField(required=True, max_length=100)

    # def create(self, validated_data):

        
    #   return APICredential.objects.create(vendor=vendor, platform=platform, access_token=access_token)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        print(validated_data['vendor__name'])

        vendor = Vendor.objects.get(name="validated_data['vendor__name']")

        platform = Vendor.objects.get(name=validated_data['platform__name'])

        obj, created = APICredential.objects.update_or_create(
            vendor=validated_data.get('vendor__name'),
            platform=validated_data.get('platform__name'),
            defaults={
                'access_token': validated_data.get('access_token')
                }
            )

        return obj

    # def update(self, instance, validated_data):

    #     if not instance.access_token:

    #         instance.access_token = validated_data.get('access_token')
            
    #         instance.save()

    #         return instance