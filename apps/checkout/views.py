from django.shortcuts import render, redirect
from apps.account.forms import LoginForm, SignUpForm
from apps.account.views import login_view_
from apps.cart.views import get_cart

# Create your views here.

def checkout_login(request):

	if request.user.is_authenticated:

		return redirect("/checkout/delivery")

	template = 'checkout/login.html'

	context = {
		'name': "Login",
		'login_form': LoginForm,
		'signup_form': SignUpForm,
		'hide_nav': True,
		'hide_cart': True,
		'cart': get_cart(request),
	}


	return login_view_(
		request, 
		template='checkout/login.html', 
		context=context, 
		redirect_url='/checkout/delivery', 
		form_type="login"
	)

def checkout_delivery(request):

	template = 'checkout/delivery.html'

	context = {
		'name': "Delivery",
		'hide_nav': True,
		'hide_cart': True,
		'cart': get_cart(request),
	}

	return render(request, template, context)

