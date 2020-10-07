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
	products = Product.objects.filter(category__id=code, product_type="parent", **filters_applied).prefetch_related('children') | Product.objects.filter(category__slug=slug, product_type="standalone", **filters_applied)


	context = {
		'category': category,
		'products': products,
		'facet_list': {
			'vendors': products.values('vendor__name').distinct().order_by('vendor__name').annotate(count=Count('vendor__name'), name=F('vendor__name')),
			'sizes': products.values('size__name').distinct().order_by('size__order').annotate(count=Count('size__name', distnct=True), name=F('size__name')),
			# 'sizes': products.filter(Q(product_type="variant")|Q(product_type="standalone")).values(),
			'colours': None,
			'jake': None,
			'josh':None,
		}
		
	}

	# .filter(Q(product_type="variant")|Q(product_type="standalone"))


	template = 'product/category.html'

	return render(request,template,context)

def product(request, slug):
	parent = Product.objects.get(slug=slug)
	children = Product.objects.filter(parent=parent)

	context = {
		'product': parent,
		'children': children,
	}
	
	template = 'product/product.html'

	return render(request, template, context)


