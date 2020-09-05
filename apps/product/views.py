from django.shortcuts import render
from apps.product.models import *

# Create your views here.

def category(request, slug):
	category = Category.objects.get(slug=slug)
	products = Product.objects.filter(category__slug=slug, product_type="parent") | Product.objects.filter(category__slug=slug, product_type="standalone")
	context = {
		'category': category,
		'products': products,
	}
	template = 'product/category.html'

	return render(request,template,context)

def product(request, slug):
	product = Product.objects.get(slug=slug)

	context = {
		'product': product,
	}

	template = 'product/product.html'

	return render(request, template, context)


