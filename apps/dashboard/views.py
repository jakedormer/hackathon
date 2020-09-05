from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.models import User as user
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UpdateDetailsForm
from .models import APICredential, Platform
from django.core.exceptions import ObjectDoesNotExist
import requests
import json
from django.views.generic import TemplateView
from json import JSONDecodeError
from .querys import *


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

				return redirect('/dashboard')

			else:

				messages.error(request, "Incorrect username or password")

				return render(request, template, context=locals())

	else:

		if request.user.is_authenticated:

			return redirect('/dashboard')

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


@login_required
def dashboard_products(request):

	vendor_object 	= request.user.profile.vendor
	platform_object = Platform.objects.get(name='shopify')
	api_credentials = APICredential.objects.get(vendor=vendor_object, platform=platform_object)


	headers = {
	      'Accept': 'application/json',
	      'Content-Type': 'application/json',
	      'X-Shopify-Storefront-Access-Token': api_credentials.access_token,
	  }

	# products(first:100, query:"product_type:coats OR product_type:'T Shirts'")

	query = """
	  {
	    shop {
	      name
	    }
	    products(first:100, query:"product_type:coats OR product_type:'T Shirts'") {
	      edges {
	        node {
	          id
	          title
	          productType
	          images(first: 1) {
	            edges {
	              node {
	                altText
	                transformedSrc
	              }
	            }
	          }
	        }
	      }
	    }
	  }


	  """
	r = requests.post("https://" + request.user.profile.vendor.name + ".myshopify.com/api/2020-04/graphql", json={'query': product_query}, headers=headers)

	json_response = r.json()

	# data = json.loads(json_response)
	products = json_response['data']['products']['edges']
	shop = json_response['data']['shop']

	print(r.json)
	print("hi" + r.text)
	print(r.status_code)

	context = {
		'products': products,

	}


	template = 'dashboard/dashboard_products.html'

	return render(request, template, context=context)


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
		'platform': 'shopify',
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

		headers = {
		      'Accept': 'application/json',
		      'Content-Type': 'application/json',
		      'X-Shopify-Storefront-Access-Token': api_credentials.access_token,
		  }


		r = requests.post("https://" + vendor_object.name + ".myshopify.com/api/2020-04/graphql", json={'query': q_productTypes}, headers=headers)

		# r = requests.get(url)
		# print(r.status_code)
		try:

			json_response = r.json()
			print(r.status_code)

			product_types = json_response['data']['shop']['productTypes']['edges']
			print(product_types)

			context['product_types'] = product_types
			

		except JSONDecodeError:
			messages.error(request, (str(r.status_code) + " - Could not connect to shopify, please check your API details are correct. Categories will appear below upon a successful connection"))
		
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

				messages.success(request, "Details Updated")

				# Update Vendor & Platform details

				# If API credentials exist, then update, else create a new object
				if api_credentials is not None:

					api_credentials.username = api_username
					api_credentials.password = api_password
					api_credentials.access_token = api_access_token


					api_credentials.save()

					initial_data['api_username'] = api_credentials.username
					initial_data['api_password'] = api_credentials.password
					initial_data['api_access_token'] = api_credentials.access_token

				else:		

					APICredential.objects.create(vendor=vendor_object, platform=platform_object, username=api_username, password=api_password, access_token=api_access_token)

				return render(request, template, context)

			else:

				print(form.errors)

				return render(request, template, context)


		# if a GET (or any other method) we'll create a blank form
	else:
		

		return render(request, template, context)

		
	# if request.POST:
	# 	name = request.POST['form_name']

	# 	if name == "update_setti":
	# 		username = request.POST['inputUsername']
	# 		password = request.POST['inputPassword']
	# 		auth_user = authenticate(request, username=username, password=password)

	# 		if auth_user is not None:

	# 			login(request, auth_user)

	# 			return redirect('/dashboard')

	# 		else:

	# 			messages.error(request, "Incorrect username or password")

	# 			return render(request, template, context=locals())

	# else:

	# 	return render(request, template, context=locals())
			


