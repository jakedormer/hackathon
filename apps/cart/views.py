from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, JsonResponse
from apps.product.models import Product
from .models import Cart, CartItem
import json

#https://docs.djangoproject.com/en/3.0/ref/django-admin/#django-admin-clearsessions
#Run as a cron job to clear up the backend

def get_cart(request, create=False):

	if request.user.is_authenticated:

		owner = request.user
	
	else:

		owner = None

	session_key = request.COOKIES.get('session_key')

	if session_key:

		try:

			cart = Cart.objects.get(owner=owner, status="open", session_key=session_key)

		except ObjectDoesNotExist:

			if create:

				cart = Cart(owner=owner, status="open", session_key=session_key)
				cart.save()
				
			else:

				cart = None

		# cart, created = Cart.objects.get_or_create(
		# 	owner=owner,
		# 	status="open",
		# 	session_key=request.COOKIES.get('session_key'),
		# 	defaults={
		# 		'owner': owner,
		# 		'status': 'open',
		# 		'session_key': request.COOKIES.get('session_key')
		# 	}
		# )

		return cart


def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result

def cart(request):

	template = 'cart/cart.html'

	cart = get_cart(request)

	context = {
		'cart': cart,
	}

	return render(request,template,context)


def add_to_cart(request):

	data = {}

	if request.method == "POST":

		params = request.POST.dict()

		product = Product.objects.get(id=params['product_id'])

		params = request.POST.dict()

		cart = get_cart(request, True)

		# Calculate quantity for cart item
		try:
			cart_item = CartItem.objects.get(cart=cart, product=product)
			current_quantity = cart_item.quantity
		except ObjectDoesNotExist:
			current_quantity=0

		# Update or create the cart item
		if current_quantity + 1 <= product.num_in_stock and product.num_in_stock != 0:

			cartitem, created = CartItem.objects.update_or_create(
				cart=cart,
				product=Product.objects.get(id=params['product_id']),
				defaults={
					'quantity': 1 + current_quantity
				}
			)

			data['add_to_cart'] = True
			data['items_in_cart'] = cart.num_items

		else:
			data['add_to_cart'] = False


		return JsonResponse(data=data)


def remove_from_cart(request):

	cart = get_cart(request)

	if request.GET:

		params = request.GET.dict()

		cart_item = CartItem.objects.get(
			cart=cart, 
			product=Product.objects.get(id=params['product_id'])
			)

		cart_item.delete()

	return redirect('/bag')


# def cart(request):

# 	# Init cart

# 	if 'cart' not in request.session:

# 		request.session['cart'] = {}
# 		request.session['cart'].setdefault('products', [])
# 		request.session['cart']['items_in_cart'] = 0

# 	cart_products = []

# 	for product in request.session['cart']['products']:

# 		cart_products.append(product['id'])

# 	products = Product.objects.filter(id__in=cart_products).order_by('vendor__name', 'category__name')
# 	print(products)

# 	context = {
# 		'products': products,
# 	}

# 	template = 'cart/cart.html'

# 	for key, value in request.session.items():
# 	    print('{} => {}'.format(key, value))

# 	return render(request,template,context)

# def add_to_cart(request):

# 	# Init Cart
# 	if 'cart' not in request.session:

# 		request.session['cart'] = {}
# 		request.session['cart'].setdefault('products', [])
# 		request.session['cart']['items_in_cart'] = 0

# 	data = {}

# 	for key, value in request.session.items():
# 		print('{} => {}'.format(key, value))

# 	if 'cart' not in request.session:

# 		request.session['cart'] = {}
# 		request.session['cart'].setdefault('products', [])


# 	if request.method == "POST":

# 		params = request.POST.dict()
# 		product_id = params['product_id']
# 		quantity = params['quantity']
# 		quantity = 1

# 		try:
# 			num_in_stock = Product.objects.get(id=product_id).stockrecords.first().num_in_stock
# 		except ObjectDoesNotExist:
# 			num_in_stock = 0

# 		exists = False

# 		# Loop through cart to check object not already in cart.
# 		for product in request.session['cart']['products']:

# 			if product['id'] == product_id:

# 				exists = True

# 				# Check cart quantity is less than stock levels.

# 				if int(product['quantity']) + int(quantity) <= num_in_stock:

# 					product['quantity'] = int(product['quantity']) + int(quantity)
# 					request.session.modified = True

# 					data['add_to_cart'] = True


# 				else:

# 					data['add_to_cart'] = False

# 				break

# 		if not exists:

# 		# Because sessions dont update unless told to.

# 			request.session['cart']['products'].append({'id': product_id, 'quantity': quantity})
# 			request.session.modified = True

# 			data['add_to_cart'] = True


# 	for key, value in request.session.items():
# 		print('{} => {}'.format(key, value))

# 	# Update the number of items in cart
		
# 	data['items_in_cart'] = 0
# 	request.session['cart']['items_in_cart'] = 0

# 	for product in request.session['cart']['products']:

# 		data['items_in_cart'] = data['items_in_cart'] + int(product['quantity'])
# 		request.session['cart']['items_in_cart'] = int(request.session['cart']['items_in_cart']) + int(product['quantity'])
# 		request.session.modified = True


# 	return JsonResponse(data=data)

# def remove_from_cart(request):

# 	for key, value in request.session.items():
# 		print('{} => {}'.format(key, value))

# 	if request.GET:

# 		params = request.GET.dict()
# 		product_id = params['product_id']

# 		for i, product in enumerate(request.session['cart']['products']):

# 			if product['id'] == product_id:

# 				print(product)
# 				del request.session['cart']['products'][i]

# 				request.session['cart']['items_in_cart'] = int(request.session['cart']['items_in_cart']) - int(product['quantity']) 

# 				request.session.modified = True

# 				print(request.session['cart']['products'])

# 				break

# 	# return JsonResponse(data={})

# 	return redirect('/cart')




