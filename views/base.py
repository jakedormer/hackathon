from django.shortcuts import render, redirect
from django.urls import reverse
from urllib.parse import urlencode
from django.core.exceptions import ObjectDoesNotExist
import re
from apps.dashboard.models import Vendor

from django.views.decorators.clickjacking import xframe_options_exempt

# Create your views here.

@xframe_options_exempt
def home(request):
	context = locals()
	template = 'home.html'

	#Shopify Oauth Install redirect
	params = request.GET.dict()

	try:
		shop_url = params['shop']

		shop_name = re.search(r'^([a-z\d_.]+)[.]myshopify[.]com[\/]?$', shop_url, re.IGNORECASE).group(1)
		query_string =  urlencode(params)
		url = "/oauth/install?" + query_string
		return redirect(url)

	except KeyError:

		return render(request,template,context)

@xframe_options_exempt
def about(request):
	context = locals()
	template = 'about.html'

	return render(request,template,context)


def privacy(request):
	context = locals()
	template = 'privacy.html'

	return render(request,template,context)