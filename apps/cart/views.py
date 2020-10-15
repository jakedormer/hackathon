from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from apps.product.models import Product
import json

def cart(request):

	if 'cart' not in request.session:

		request.session['cart'] = {}
		request.session['cart'].setdefault('products', [])
		request.session['cart']['items_in_cart'] = 0

	cart_products = []

	for product in request.session['cart']['products']:

		cart_products.append(product['id'])

	products = Product.objects.filter(id__in=cart_products).order_by('vendor__name')

	context = {
		'products': products,
	}

	template = 'cart/cart.html'

	for key, value in request.session.items():
	    print('{} => {}'.format(key, value))

	return render(request,template,context)

def add_to_cart(request):

	# request.session.flush()

	for key, value in request.session.items():
	    print('{} => {}'.format(key, value))

	if 'cart' not in request.session:

		request.session['cart'] = {}
		request.session['cart'].setdefault('products', [])


	if request.GET:

		params = request.GET.dict()
		product_id = params['product_id']
		quantity = params['quantity']
		print(product_id)
		
		exists = False

		# Loop through cart to check object not already in cart
		for product in request.session['cart']['products']:

			if product['id'] == product_id:

				exists = True
				
				product['quantity'] = int(product['quantity']) + int(quantity)
				request.session.modified = True

				break

		if not exists:

		# Because sessions dont update sometimes	

			request.session['cart']['products'].append({'id': product_id, 'quantity': quantity})
			request.session.modified = True

	for key, value in request.session.items():
	    print('{} => {}'.format(key, value))

	    request.session['cart']['items_in_cart'] = len(request.session['cart']['products'])

	return JsonResponse(data={})
