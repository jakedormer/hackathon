from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from apps.account.forms import SignUpForm
from apps.dashboard.models import Vendor
from apps.cart.models import Cart
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from apps.cart.views import get_cart
import json

# Create your views here.
@login_required
def account_orders(request):

	template = "account/account_orders.html"

	context = {}

	return render(request, template, context)

@login_required
def account_favourites(request):

	template = "account/account_favourites.html"

	context = {}

	return render(request, template, context)

@login_required()
def logout_view(request):

	logout(request)
	# Redirect to a success page.

	messages.warning(request, "You are now logged out", extra_tags="alert-warning")

	return redirect('/login')

def login_cart_logic(request, user):

	"""
	If user goes from unauth to auth, we need to make sure that the existing cart 
	is removed and replaced with the new one. We might even add the products to a
	wishlist in future.
	"""
	print("hi")
	print(request.COOKIES.get('session_key'))
	print(user)

	auth_bag = Cart.objects.get(owner=user, status="open")


	print(auth_bag)

	unauth_bag = Cart.objects.get(owner=None, status="open", session_key=request.COOKIES.get('session_key'))
	

	print(unauth_bag)

	if unauth_bag and auth_bag:

		auth_bag.delete()

	# Mark the unauth bag with its owner
	unauth_bag.owner = user
	unauth_bag.save()


def login_view_(request, template, context, redirect_url, vendor, form_type):

	"""
	Used as a general login view for both cart login and standard login

	"""


	if not context:
		context = {}
	# template = 'account/login.html'
	
	if request.POST and request.POST['form_name'] == "login":

		username = request.POST['username']
		password = request.POST['password']

		context['username'] = username

		auth_user = authenticate(request, username=username, password=password)

		if auth_user is not None:

			if not auth_user.profile.is_vendor:

				login(request, auth_user)

				login_cart_logic(request, auth_user)

				return redirect(redirect_url)

			else:

				messages.error(request, "This is a vendor account and cannot login here", extra_tags="alert-danger")

		else:

			messages.error(request, "Incorrect username or password", extra_tags="alert-danger")

		context['type'] = form_type
		
	else:

		if request.user.is_authenticated and vendor:

			return redirect(redirect_url)

	return render(request, template, context)

def login_view(request):

	return login_view_(request, template='account/login.html', context={}, redirect_url='/account/orders', vendor=False, form_type="login")


def login_vendor(request):

	context = {
		'hide_nav': True,
		'hide_cart': True,
	}

	template = 'account/login_vendor.html'

	if request.POST:

		context['username'] = request.POST['username']
		username = request.POST['username']
		password = request.POST['password']

		auth_user = authenticate(request, username=username, password=password)

		if auth_user is not None:

			if auth_user.profile.is_vendor:

				login(request, auth_user)
				
				context['token'] = request.user.auth_token.key

				messages.error(request, "Login successful, you can now close this window", extra_tags="alert-success")


			else:

				messages.error(request, "This is a customer account and cannot login here", extra_tags="alert-danger")

		else:

			messages.error(request, "Incorrect username or password", extra_tags="alert-danger")

		
	else:

		# if request.user.is_authenticated and request.user.profile.is_vendor:

		# 	context['token'] = request.user.auth_token.key

		# 	messages.error(request, "You are already logged in, please close this window", extra_tags="alert-success")

		pass


	return render(request, template, context)



def create_account(request):

	template = 'account/create-account.html'

	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.refresh_from_db()  # load the profile instance created by the signal
			user.profile.email_pref = form.cleaned_data.get('email_pref')
			user.profile.sms_pref = form.cleaned_data.get('sms_pref')
			user.save()

			password1 = form.cleaned_data.get('password1')

			user = authenticate(username=user.username, password=password1)
			login(request, user)
			messages.success(request, "Account created", extra_tags="alert-success")
			return redirect('/login')


		else:
			errors = form.errors.as_json()
			errors = json.loads(errors).items() # Convert string to json dictionary
			string = ""

			for x in errors:
				string += x[0].upper() + ": " + x[1][0]['message'] + "\n"
				print(x[0], x[1][0]['message'])

			messages.error(request, string, extra_tags="alert-danger")

			return render(request, template, {'form': form})

	else:

		form = SignUpForm()

		if request.user.is_authenticated:
			return redirect('/login')

		else:
			return render(request, template, {'form': form})

def add_to_favourites(request):

	if request.method == 'POST':

		data = {}
		vendor = request.POST['vendor']
		vendor = Vendor.objects.get(name=vendor)

		if request.user.profile.favourites.all().filter(name=vendor.name).exists():

			data['add_to_favourites'] = False

			request.user.profile.favourites.remove(vendor)

		else:

			request.user.profile.favourites.add(vendor)

			data['add_to_favourites'] = True

		return JsonResponse(data)

	



