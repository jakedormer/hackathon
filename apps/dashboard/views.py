from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.models import User as user
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UpdateDetailsForm
from .models import APICredential, Platform, Vendor
from django.core.exceptions import ObjectDoesNotExist
import requests
import json
from django.views.generic import TemplateView
from json import JSONDecodeError
from .querys import *
from apps.product.models import Product


# Create your views here.
def login_view(request):

	template = 'dashboard/login.html'
	
	if request.POST:
		name = request.POST['form_name']

		if name == "login":
			username = request.POST['inputUsername']
			password = request.POST['inputPassword']
			auth_user = authenticate(request, username=username, password=password)

			if auth_user is not None:

				login(request, auth_user)

				return redirect('/dashboard/products')

			else:

				messages.error(request, "Incorrect username or password")

				return render(request, template, context=locals())

	else:

		if request.user.is_authenticated:

			return redirect('/dashboard/products')

		else:

			return render(request, template, context=locals())



@login_required()
def logout_view(request):

	logout(request)
	# Redirect to a success page.

	messages.warning(request, "You are now logged out")

	return redirect('/login')

@login_required()
def dashboard(request):

	template = 'dashboard/dashboard.html'
	return render(request, template, context=locals())

@login_required()
def dashboard_sizes(request):

	template = 'dashboard/dashboard_sizes.html'
	return render(request, template, context=locals())

@login_required()
def dashboard_sizes_create(request):

	template = 'dashboard/dashboard_sizes_create.html'
	return render(request, template, context=locals())

@login_required
def dashboard_products(request):

	vendor = request.user.profile.vendor
	products = Product.objects.filter(vendor=vendor).order_by('title',)

	context = {
		'products': products,
	}


	template = 'dashboard/dashboard_products.html'

	return render(request, template, context=context)


def api_connect(platform, vendor_name, access_token, query):

	headers = {
	      'Accept': 'application/json',
	      'Content-Type': 'application/json',
	      'X-Shopify-Storefront-Access-Token': access_token,
	  }


	r = requests.post("https://" + vendor_name + ".myshopify.com/api/2020-04/graphql", json={'query': query}, headers=headers)

	try:

		json_response = r.json()
		# print(r.status_code)

		data = json_response['data']
		# print(data)

		return [r.status_code, data]

	except JSONDecodeError:

		return [r.status_code, " - Could not connect to shopify, please check your API details are correct. Categories will appear below upon a successful connection"]

@login_required
def dashboard_settings(request):

	context = {}
	api_credentials = None

	template = 'dashboard/dashboard_settings.html'
	initial_data = {
		'first_name': request.user.first_name,
		'surname': request.user.last_name,
		'email': request.user.email,
		'vendor': request.user.profile.vendor.name,
		'platform': 'Shopify',
	}

	platform_object = Platform.objects.get(name='shopify')


	# See if vendor platform exists and then populate initial data and check API is working
	try:

		vendor_object 	= request.user.profile.vendor
		api_credentials = APICredential.objects.get(vendor=vendor_object, platform=platform_object)

		initial_data['api_username'] = api_credentials.username
		initial_data['api_password'] = api_credentials.password
		initial_data['api_access_token'] = api_credentials.access_token

		# Run API to shopify to get collections

	except ObjectDoesNotExist:
		pass

	form = UpdateDetailsForm(initial=initial_data)

	context['form'] = form

	if request.method == 'POST':
			# create a form instance and populate it with data from the request:
			form = UpdateDetailsForm(request.POST)

			# check whether it's valid:
			if form.is_valid():
				first_name 		= form.cleaned_data['first_name']
				surname			= form.cleaned_data['surname']
				email			= form.cleaned_data['email']
				platform 		= form.cleaned_data['platform']
				api_username 	= form.cleaned_data['api_username']
				api_password	= form.cleaned_data['api_password']
				api_access_token= form.cleaned_data['api_access_token']

				# Update user object

				request.user.first_name = first_name
				request.user.last_name = surname
				request.user.email = email

				request.user.save()

				messages.info(request, "Details Updated")

				# Update Vendor & Platform details

				# If API credentials exist, then update, else create a new object
				if api_credentials is not None:

					api_credentials.username = api_username
					api_credentials.password = api_password
					api_credentials.access_token = api_access_token


					api_credentials.save()

					initial_data['first_name'] = request.user.first_name
					initial_data['surname'] = request.user.last_name
					initial_data['email'] = request.user.email

					initial_data['api_username'] = api_credentials.username
					initial_data['api_password'] = api_credentials.password
					initial_data['api_access_token'] = api_credentials.access_token

				else:		

					APICredential.objects.create(vendor=vendor_object, platform=platform_object, username=api_username, password=api_password, access_token=api_access_token)


				c = api_connect(platform='shopify', vendor_name=vendor_object.name, access_token = api_access_token, query=q_productTypes)

				if c[0] == 200:
					context['product_types'] = c[1]['shop']['productTypes']['edges']
					messages.success(request, 'API connected successfully')
				else:
					messages.error(request, str(c[0]) + c[1])
				
				return render(request, template, context)
					

			else:

				print(form.errors)

				return render(request, template, context)


		# if a GET (or any other method) we'll create a blank form
	else:

		c = api_connect(platform='shopify', vendor_name=vendor_object.name, access_token = api_credentials.access_token, query=q_productTypes)

		if c[0] == 200:
			context['product_types'] = c[1]['shop']['productTypes']['edges']
			messages.success(request, 'API connected successfully')
		else:
			 messages.error(request, str(c[0]) + c[1])
		
		return render(request, template, context)

	
			


