from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth.models import User as user
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UpdateDetailsForm
from .models import Platform, Vendor
from django.core.exceptions import ObjectDoesNotExist
import requests
import json
from django.views.generic import TemplateView
from json import JSONDecodeError
from .querys import *
from apps.product.models import Product, Category, Size, SizeGuide, SizeGuideItem, Attribute
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Q
import re




# @login_required()
# def dashboard(request):

# 	template = 'dashboard/dashboard.html'
# 	return render(request, template, context=locals())


# @login_required()
# def dashboard_sizes(request):

# 	size_guides = SizeGuide.objects.filter(vendor=request.user.profile.vendor).order_by('category', 'name').annotate(count=Count('product'))

# 	context = {
# 		'sgs': size_guides,
# 	}

# 	template = 'dashboard/dashboard_sizes.html'
# 	return render(request, template, context)


# @login_required()
# def dashboard_sizes_create(request):

# 	template = 'dashboard/dashboard_sizes_create.html'
# 	categories = Category.objects.all().order_by("name")
# 	sizes = Size.objects.all().order_by("order")
# 	attributes = Attribute.objects.all()

# 	if 'id' in request.GET:

# 		try:
# 			id = request.GET["id"]
# 			size_guide = SizeGuide.objects.filter(vendor=request.user.profile.vendor, id=id).first()

# 		except ValueError:
# 			id = None
# 			size_guide = None
# 	else:
# 		id = None
# 		size_guide = None

# 	context = {
# 		'categories': categories,
# 		'sizes': sizes,
# 		'size_guide': size_guide,
# 		'attributes': attributes,
# 	}

# 	if request.method == 'POST':

# 		params = request.POST
# 		category = Category.objects.get(name=params['category'].lower())
# 		# If size guide already exists, then update with new values

# 		try:
# 			if size_guide:
# 				name = size_guide.name
# 				size_guide.name = params['name']
# 				size_guide.category = category
# 				size_guide.save()
# 				sg_obj = None

# 			else:
# 				print("hi")
# 				sg_obj = SizeGuide(
# 					name=params['name'],
# 					vendor=request.user.profile.vendor,
# 					category=category,
# 					)
				
# 				sg_obj.save()

# 				size_guide = sg_obj

# 		except IntegrityError:

# 			messages.error(request, "Size guide names must be unique", extra_tags="alert-danger")

# 			return render(request, template, context)
			
# 		for key in request.POST:
# 			if re.search(r'\|', key, re.IGNORECASE):

# 				size = key.split('|')[0]
# 				attribute = key.split('|')[1]

# 				# If size guide measurement is not null, then create or update sizeguide item
# 				if request.POST[key]:
# 					sgi_obj, sgi_created = SizeGuideItem.objects.update_or_create(
# 						size_guide = size_guide,
# 						size = Size.objects.get(value=size),
# 						attribute = Attribute.objects.get(name=attribute),
# 						defaults = {
# 							'value': request.POST[key]
# 							}
# 						)

# 				context[key] = request.POST[key]

# 		if sg_obj:

# 			messages.success(request, "Size guide created successfully.", extra_tags="alert-success")

# 		else:

# 			messages.success(request, "Size guide updated successfully.", extra_tags="alert-success")

# 		context['size_guide'] = size_guide


# 	return render(request, template, context)

# @login_required
# def dashboard_sizes_delete(request, code):

# 	if request.method == 'POST' and request.POST['form_name'] == 'delete_size_guide':
# 		print("hi")

# 		size_guide = SizeGuide.objects.get(
# 			vendor=request.user.profile.vendor,
# 			id=code
# 			)


# 		size_guide.delete()


# 	return redirect('/dashboard/sizes')

# @login_required
# def apply_size_guide(request):
# 	if request.method == "POST":

# 		product = Product.objects.get(vendor=request.user.profile.vendor, id=request.POST['product'])

# 		if request.POST['size_guide_name']:

# 			size_guide = SizeGuide.objects.filter(vendor=request.user.profile.vendor, name=request.POST['size_guide_name']).first()

# 			product.size_guide = size_guide
# 			product.save()

# 			data = {
# 				'updated': True
# 			}

# 			# Else, remove the relationship
# 		else:
# 			product.size_guide = None
# 			product.save()

# 			data = {
# 				'created': True
# 			}

		

# 		return JsonResponse(data)

# @login_required
# def dashboard_products(request):

# 	vendor = request.user.profile.vendor
# 	products = Product.objects.filter(Q(vendor=vendor) & (Q(product_type="parent") | Q(product_type="standalone"))).order_by('title')
# 	size_guides = SizeGuide.objects.filter(vendor=vendor).order_by('name')

# 	context = {
# 		'products': products,
# 		'size_guides': size_guides,
# 	}


# 	template = 'dashboard/dashboard_products.html'

# 	return render(request, template, context=context)


# def api_connect(platform, vendor_name, access_token, query):

# 	headers = {
# 	      'Accept': 'application/json',
# 	      'Content-Type': 'application/json',
# 	      'X-Shopify-Storefront-Access-Token': access_token,
# 	  }


# 	r = requests.post("https://" + vendor_name + ".myshopify.com/api/2020-04/graphql", json={'query': query}, headers=headers)

# 	try:

# 		json_response = r.json()
# 		# print(r.status_code)

# 		data = json_response['data']
# 		# print(data)

# 		return [r.status_code, data]

# 	except JSONDecodeError:
# 		print(r.content)
# 		return [r.status_code, " - Could not connect to shopify, please check your API details are correct. Categories will appear below upon a successful connection"]

# @xframe_options_exempt
# @login_required
# def dashboard_settings(request):

# 	context = {}
# 	api_credentials = None

# 	template = 'dashboard/dashboard_settings.html'
# 	initial_data = {
# 		'first_name': request.user.first_name,
# 		'surname': request.user.last_name,
# 		'email': request.user.email,
# 		'vendor': request.user.profile.vendor.name,
# 		'platform': 'Shopify',
# 	}

# 	platform_object = Platform.objects.get(name='shopify')


# 	# See if vendor platform exists and then populate initial data and check API is working
# 	try:

# 		vendor_object 	= request.user.profile.vendor
# 		api_credential = APICredential.objects.get(vendor=vendor_object, platform=platform_object)


# 	except ObjectDoesNotExist:
# 		pass

# 	form = UpdateDetailsForm(initial=initial_data)

# 	context['form'] = form

# 	if request.method == 'POST':
# 			# create a form instance and populate it with data from the request:
# 			form = UpdateDetailsForm(request.POST)

# 			# check whether it's valid:
# 			if form.is_valid():
# 				first_name 		= form.cleaned_data['first_name']
# 				surname			= form.cleaned_data['surname']
# 				email			= form.cleaned_data['email']
# 				platform 		= form.cleaned_data['platform']

# 				# Update user object

# 				request.user.first_name = first_name
# 				request.user.last_name = surname
# 				request.user.email = email

# 				initial_data['first_name'] = first_name
# 				initial_data['surname'] = surname
# 				initial_data['email'] = email

# 				request.user.save()

# 				messages.info(request, "Details Updated")


# 	# if a GET (or any other method) we'll create a blank form
# 	print(vendor_object.name)
# 	print(api_credential.access_token)
# 	print(q_productTypes)
# 	c = api_connect(platform='shopify', vendor_name=vendor_object.name, access_token=api_credential.access_token, query=q_productTypes)

# 	if c[0] == 200:
# 		context['product_types'] = c[1]['shop']['productTypes']['edges']
# 		messages.success(request, 'API connected successfully')
# 	else:
# 		 print(c[0])
# 		 messages.error(request, str(c[0]) + c[1])
	
# 	return render(request, template, context)

	
			


