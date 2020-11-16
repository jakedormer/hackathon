from apps.product.models import Category, Product
from apps.cart.models import Cart
from django.template.loader import get_template
from django import template
from apps.cart.views import get_cart

register = template.Library()


def categories(request):
    
    return {
    	'all_categories': Category.objects.all().order_by('name')
    }

def cart_count(request):

	cart = get_cart(request)

	if cart:

		cart_count = cart.num_items

	else:
		
		cart_count = 0

	return {
		'cart_count': cart_count
	}


