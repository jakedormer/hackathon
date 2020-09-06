from django.shortcuts import render
from apps.product.models import *

# Create your views here.

def category(request, slug):
	category = Category.objects.get(slug=slug)
	products = Product.objects.filter(category__slug=slug, product_type="parent") | Product.objects.filter(category__slug=slug, product_type="standalone")
	context = {
		'category': category,
		'filters': category.attributegroup_set.all(),
		'products': products,
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


