from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import login_required

# Create your views here.
# Create your views here.
@xframe_options_exempt
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

				login(request, auth_user)

				return redirect('/dashboard/products')

			else:

				messages.error(request, "Incorrect username or password", extra_tags="alert-danger")

				return render(request, template, context)

	else:

		if request.user.is_authenticated:

			return redirect('/dashboard/products')

		else:

			return render(request, template, context)



@login_required()
def logout_view(request):

	logout(request)
	# Redirect to a success page.

	messages.warning(request, "You are now logged out", extra_tags="alert-warning")

	return redirect('/login')