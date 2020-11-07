from django.shortcuts import render, redirect
from django.urls import reverse
from urllib.parse import urlencode
from django.core.exceptions import ObjectDoesNotExist
import re
from apps.dashboard.models import Vendor
from apps.product.models import Category, Product
from django.db.models import Q

# Create your views here.
def home(request):
	context = {}
	template = 'base/home.html'
	categories = Category.objects.all().order_by('name')
	context['categories'] = categories
	context['tshirts'] = Product.objects.filter((Q(product_type="parent") | Q(product_type="standalone")), category_id=1)

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

def about(request):
	context = locals()
	template = 'base/about.html'

	return render(request,template,context)


def privacy(request):
	context = locals()
	template = 'base/privacy.html'

	return render(request,template,context)