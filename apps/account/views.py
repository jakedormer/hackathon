from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Create your views here.
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

				else:

					messages.error(request, "This is a customer account and cannot login here", extra_tags="alert-danger")

			else:

				messages.error(request, "Incorrect username or password", extra_tags="alert-danger")

	else:

		if request.user.is_authenticated:

			return redirect('/dashboard/products')

	return render(request, template, context)


def login_vendor(request):

	template = 'account/login_vendor.html'

	if request.POST:
		name = request.POST['form_name']

		if name == "login":
			context['username'] = request.POST['inputUsername']
			username = request.POST['inputUsername']
			password = request.POST['inputPassword']

			auth_user = authenticate(request, username=username, password=password)

			if auth_user is not None:

				if auth_user.profile.is_vendor:

					print("hi")

					login(request, auth_user)

					response = render(request, 'dashboard/dashboard_products.html', context)

					return response

				else:

					messages.error(request, "This is a vendor account and cannot login here", extra_tags="alert-danger")

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

	return render(request, template, context=locals())



