from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from apps.account.forms import SignUpForm
from apps.dashboard.models import Vendor
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
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


def login_view(request):

	context = {}
	template = 'account/login.html'
	
	if request.POST:
		name = request.POST['form_name']

		if name == "login":
			context['username'] = request.POST['inputUsername']
			username = request.POST['inputUsername']
			password = request.POST['inputPassword']

			auth_user = authenticate(request, username=username, password=password)

			if auth_user is not None:

				if not auth_user.profile.is_vendor:

					login(request, auth_user)

					return redirect("/account/orders")

				else:

					messages.error(request, "This is a vendor account and cannot login here", extra_tags="alert-danger")

			else:

				messages.error(request, "Incorrect username or password", extra_tags="alert-danger")

	else:

		if request.user.is_authenticated:

			return redirect('/account/orders')

	return render(request, template, context)


def login_vendor(request):

	context = {}
	template = 'account/login_vendor.html'

	if request.POST:
		name = request.POST['form_name']

		if name == "login":
			context['username'] = request.POST['inputUsername']
			username = request.POST['inputUsername']
			password = request.POST['inputPassword']

			auth_user = authenticate(request, username=username, password=password)

			if auth_user is not None:
				print(auth_user.profile.is_vendor)

				if auth_user.profile.is_vendor:

					login(request, auth_user)

					response = render(request, 'dashboard/dashboard_products.html', context)

					return response

				else:

					messages.error(request, "This is a customer account and cannot login here", extra_tags="alert-danger")

			else:

				messages.error(request, "Incorrect username or password", extra_tags="alert-danger")

	else:

		if request.user.is_authenticated:

			return redirect('/dashboard/products')

	return render(request, template, context)



@login_required()
def logout_view(request):

	logout(request)
	# Redirect to a success page.

	messages.warning(request, "You are now logged out", extra_tags="alert-warning")

	return redirect('/login')

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

	



