from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.dashboard.models import Vendor
from .serializers import UserSerializer, VendorSerializer
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework import generics
from rest_framework.parsers import JSONParser
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


class CurrentUser(APIView):

	authentication_classes = [TokenAuthentication,]

	def get(self, request):
		user = request.user
		serializer = UserSerializer(user)
		return Response(serializer.data)

class VendorAPI(APIView):

	authentication_classes = [TokenAuthentication,]

	def get(self, request):

		data = JSONParser().parse(request)
		user = request.user

		try:
			vendor = Vendor.objects.get(name=data['name'])
			
		except ObjectDoesNotExist:

			return JsonResponse({"detail": "Vendor does not exist"}, status=400)


		serializer = VendorSerializer(vendor, data=data)

		if user:

			if serializer.is_valid():
			
				return JsonResponse(serializer.data)
			
			return JsonResponse(serializer.errors, status=400)

		else:

			return JsonResponse({"detail": "Invalid token account."}, status=400)

	# def post(self, request):
	# 	return self.update(request, *args, **kwargs)

	# def post(self, request):
	# 	data = JSONParser().parse(request)
	# 	user = request.user
	# 	vendor = request.user.profile.vendor
	# 	serializer = VendorSerializer(vendor, data=data)

	# 	if serializer.is_valid():

	# 		serializer.save()
			
	# 		return JsonResponse(serializer.data)
			
	# 	return JsonResponse(serializer.errors, status=400)

	def post(self, request):

		data = JSONParser().parse(request)
		user = request.user

		try:
			vendor = Vendor.objects.get(name=data['name'])

		except ObjectDoesNotExist:

			return JsonResponse({"detail": "Vendor does not exist"}, status=400)


		serializer = VendorSerializer(vendor, data=data)

		"""
		This call is made when a user installs shopify and thus doesn't have a user token yet. 
		As such we use the token mapped to the account in settings.ALLOWED_EMAIL
		"""

		if user.username == settings.ALLOWED_EMAIL:

			if serializer.is_valid():

				serializer.save()
			
				return JsonResponse(serializer.data)
			
			return JsonResponse(serializer.errors, status=400)

		else:

			return JsonResponse({"detail": "Invalid token account."}, status=400)

		


		



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

