from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, APICredentialSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes
from apps.dashboard.models import APICredential
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework import mixins
from rest_framework import generics
from rest_framework.parsers import JSONParser


class CurrentUser(APIView):

	authentication_classes = [TokenAuthentication,]

	def get(self, request):
		user = request.user
		serializer = UserSerializer(user)
		return Response(serializer.data)


class AccessToken(APIView):
	
	serializer_class = APICredentialSerializer
	authentication_classes = [BasicAuthentication,]

	def get_queryset(self):
		"""
		Optionally restricts the returned purchases to a given user,
		by filtering against a `username` query parameter in the URL.
		"""
		vendor__name = self.request.query_params.get('vendor__name')
		print(vendor__name)
		platform__name = self.request.query_params.get('platform__name')
		print(platform__name)

		queryset = APICredential.objects.filter(vendor__name=vendor__name, platform__name=platform__name).first()
		print(queryset)

		return queryset
	

	@csrf_exempt
	def post(self, request, *args, **kwargs):

		serializer = APICredentialSerializer(data=request.query_params)

		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

		# instance = self.get_queryset()
		# print(instance)

		# if not instance.access_token:

		# 	instance.access_token = validated_data.get('access_token', instance.access_token)
			
		# 	instance.save()

		# 	return return JsonResponse("Model Updated")

		



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




@api_view(['POST'])
def update_shopify_token(request):

	user = request.user
	vendor = user.vendor

	obj, created = APICredential.objects.update_or_create(
		platform__name='shopify',
		vendor=vendor,
		defaults = {
			'access_token': '1',
		}

	)

	return
