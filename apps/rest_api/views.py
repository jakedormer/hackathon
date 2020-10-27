from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from apps.dashboard.models import APICredential
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication


class CurrentUser(APIView):

	authentication_classes = [TokenAuthentication,]

	def get(self, request):
		user = request.user
		serializer = UserSerializer(user)
		return Response(serializer.data)


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
