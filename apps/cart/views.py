from django.shortcuts import render

def cart(request):
	context = locals()
	template = 'cart/cart.html'

	return render(request,template,context)
