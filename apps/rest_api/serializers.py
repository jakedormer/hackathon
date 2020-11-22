from django.contrib.auth.models import User
from rest_framework import serializers
from apps.dashboard.models import Vendor, Platform

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['name', 'api_access_token', 'num_items', 'num_items_published']
        read_only_fields = ['name', 'num_items', 'num_items_published']


    def update(self, instance, validated_data):
        instance.api_access_token = validated_data['api_access_token']
        instance.save()
        return instance


