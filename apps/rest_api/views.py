from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, VendorSerializer
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework import generics
from rest_framework.parsers import JSONParser


class CurrentUser(APIView):

	authentication_classes = [TokenAuthentication,]

	def get(self, request):
		user = request.user
		serializer = UserSerializer(user)
		return Response(serializer.data)

class Vendor(APIView):

	authentication_classes = [TokenAuthentication,]

	def get(self, request):
		user = request.user
		vendor = request.user.profile.vendor
		serializer = VendorSerializer(vendor)
		return Response(serializer.data)

	def post(self, request):
		data = JSONParser().parse(request)
		user = request.user
		vendor = request.user.profile.vendor
		serializer = VendorSerializer(vendor, data=data)

		if serializer.is_valid():

			serializer.save()
			
			return JsonResponse(serializer.data)
			
		return JsonResponse(serializer.errors, status=400)
		
		

		



# @api_view(['POST'])
# @authentication_classes([BasicAuthentication,])
# def AccessToken(request):

# 	authentication_classes = [BasicAuthentication,]

# 	if request.method == "POST":

# 		data = JSONParser().parse(request)
# 		serializer = APICredentialSerializer(data=data)

# 		if serializer.is_valid():
# 			serializer.save()

# 			return JsonResponse(serializer.data) 
# 		return JsonResponse(serializer.errors)

