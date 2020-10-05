from django.shortcuts import render
from apps.product.models import *
from django.db.models import Count
from django.db.models import F

# Create your views here.

def category(request, slug):
	category = Category.objects.get(slug=slug)
	products = Product.objects.filter(category__slug=slug, product_type="parent") | Product.objects.filter(category__slug=slug, product_type="standalone")
	
	context = {
		'category': category,
		'filters': category.categoryattributegroup_set.all(),
		'products': products,
		'facet_list': {
			'Brands': products.values('vendor__name').distinct().order_by('vendor__name').annotate(count=Count('vendor__name', distnct=True)),
			'Sizes': products.values('size__value').distinct().order_by('size__order').annotate(count=Count('size__value', distnct=True)),
			'Colours': None,
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


