from django.shortcuts import render
from apps.product.models import *
from django.db.models import Count, F, Q


# Create your views here.

def category(request, slug, code):
	filters_applied = {}
	
	if 'vendors' in request.GET:
		filters_applied['vendor__name'] = request.GET['vendors']

	
	if 'sizes' in request.GET:
		filters_applied['size__name'] = request.GET['sizes']

	category = Category.objects.get(id=code)
	# products = Product.objects.filter(
	# 	category__name="t-shirts", 
	# 	product_type="parent", 
	# 	# **filters_applied
	# 	).prefetch_related('children') | Product.objects.filter(category__name="t-shirts", product_type="standalone", 
	# 	# **filters_applied
	# 	)

	products = Product.objects.filter(
		category=category,
		)

	
	attribute_values = AttributeValue.objects.filter(product__in=products)
	
	print(attribute_values.values())

	context = {
		'category': category,
		'products': products.filter(Q(product_type="parent") | Q(product_type="standalone")),
		'facet_list': {
			'brands': attribute_values.filter(Q(product__product_type="parent") | Q(product__product_type="standalone"), attribute__name="brand").values('value_text').distinct().order_by('value_text').annotate(count=Count('value_text'), name=F('value_text')),
			'sizes':  attribute_values.filter(attribute__name="size").values('attribute__name').order_by('value_text').annotate(count=Count('value_text'), name=F('value_text')),
			# 'sizes': products.filter(Q(product_type="variant")|Q(product_type="standalone")).values(),
			'colours': None,
		}
		
	}

	# .filter(Q(product_type="variant")|Q(product_type="standalone"))


	template = 'product/category.html'

	return render(request,template,context)

def product(request, id):
	product = Product.objects.get(id=id)
	variants = product.children.all()

	if variants:
		sizes = AttributeValue.objects.filter(attribute__name="size", product__in=product.children.all()).order_by('value_option__order')
	else:
		sizes = AttributeValue.objects.filter(attribute__name="size", product=product).order_by('value_option__order')

	print(sizes)
	print(variants)

	context = {
		'product': product,
		'sizes': sizes,
	}
	

	template = 'product/product.html'

	return render(request, template, context)


