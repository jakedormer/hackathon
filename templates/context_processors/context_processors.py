from apps.product.models import Category, Product
from apps.cart.models import Cart
from django.template.loader import get_template
from django import template

register = template.Library()


def categories(request):
    
    return {
    	'all_categories': Category.objects.all().order_by('name')
    }

def cart_count(request):

	if request.user.is_authenticated:

		try:
			cart_count = Cart.objects.filter(owner=request.user, status='open').first().num_items
		except AttributeError:
			cart_count = 0
	else:

		try:
			cart_count = Cart.objects.filter(status='open', session_key=request.COOKIES.get('session_key')).first().num_items
		except AttributeError:
			cart_count = 0

	return {
		'cart_count': cart_count
	}


