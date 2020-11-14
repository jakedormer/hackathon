from django.shortcuts import render
from apps.account.forms import LoginForm, SignUpForm
from apps.account.views import login_view_

# Create your views here.

def checkout_login(request):

	template = 'checkout/login.html'

	context = {
		'login_form': LoginForm,
		'signup_form': SignUpForm,
		'hide_nav': True,
		'hide_cart': True,
	}


	return login_view_(
		request, 
		template='checkout/login.html', 
		context=context, 
		redirect_url='/checkout/delivery', 
		vendor=False, 
		form_type="login"
	)

def checkout_delivery(request):

	template = 'checkout/delivery.html'

	context = {
		'checkout': True,
	}

	return render(request, template, context)

