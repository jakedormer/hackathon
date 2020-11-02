from apps.product.models import Category
from apps.cart.models import Cart

def categories(request):
    
    return {
    	'all_categories': Category.objects.all().order_by('name')
    }

def cart_count(request):

	return {
		'cart_count': Cart.objects.filter(user=request.user, status='open').first()
	}