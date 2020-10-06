from django.shortcuts import render
from apps.product.models import *
from django.db.models import Count
from django.db.models import F

# Create your views here.

def category(request, slug, code):
	filters_applied = {}
	if 'vendors' in request.GET:
		filters_applied['vendor__name'] = request.GET['vendors']
		print("hi")

	category = Category.objects.get(id=code)
	products = Product.objects.filter(category__id=code, product_type="parent", **filters_applied) | Product.objects.filter(category__slug=slug, product_type="standalone", **filters_applied)
	
	context = {
		'category': category,
		'filters': category.categoryattributegroup_set.all(),
		'products': products,
		'facet_list': {
			'vendors': products.values('vendor__name').distinct().order_by('vendor__name').annotate(count=Count('vendor__name', distnct=True)),
			'sizes': products.values('size__value').distinct().order_by('size__order').annotate(count=Count('size__value', distnct=True)),
			'colours': None,
		}
		
	}



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


