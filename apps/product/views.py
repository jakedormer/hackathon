from django.shortcuts import render
from apps.product.models import *
from django.db.models import Count, F, Q
from django.core.paginator import Paginator



# Create your views here.

def category(request, slug, code):
	filters_applied = {}
	other_filter = {}
	
	if 'brands' in request.GET:
		filters_applied['product__vendor__name'] = request.GET['brands']

	
	if 'sizes' in request.GET:
		filters_applied['value_text'] = request.GET['sizes']

	category = Category.objects.get(id=code)
	# products = Product.objects.filter(
	# 	category__name="t-shirts", 
	# 	product_type="parent", 
	# 	# **filters_applied
	# 	).prefetch_related('children') | Product.objects.filter(category__name="t-shirts", product_type="standalone", 
	# 	# **filters_applied
	# 	)

	if len(filters_applied) > 0:
		products = Product.objects.filter(
			category=category,
			attribute_values__in=AttributeValue.objects.filter(**filters_applied)
			)
	else:

		products = Product.objects.filter(
			category=category,
			# attribute_values__in=AttributeValue.objects.filter(**filters_applied)
			)

	
	attribute_values = AttributeValue.objects.filter(product__in=products)
	# print("filter", filters_applied)
	# print(products)
	# print(attribute_values.values())

	products = products.filter(Q(product_type="parent") | Q(product_type="standalone"))
	paginator = Paginator(products, 4)
	page_number = request.GET.get('page')
	products = paginator.get_page(page_number)

	context = {
		'category': category,
		'products': products,
		'facet_list': {
			'brands': attribute_values.filter(Q(product__product_type="parent") | Q(product__product_type="standalone"), attribute__name="brand").values('value_text').distinct().order_by('value_text').annotate(count=Count('value_text'), name=F('value_text')),
			'sizes':  attribute_values.filter(attribute__name="size").values('attribute__name').order_by('value_text').annotate(count=Count('value_text'), name=F('value_text')),
			# 'sizes': products.filter(Q(product_type="variant")|Q(product_type="standalone")).values(),
			'colours': None,
			'jake': None
		}
		
	}

	# .filter(Q(product_type="variant")|Q(product_type="standalone"))


	template = 'product/category.html'

	return render(request,template,context)

def product(request, id):
	product = Product.objects.get(id=id)
	variants = product.children.all()
	related_items = Product.objects.filter((Q(product_type="parent") | Q(product_type="standalone")), category=product.category).exclude(id=product.id)

	if variants:
		sizes = AttributeValue.objects.filter(attribute__name="size", product__in=product.children.all()).order_by('value_option__order')
	else:
		sizes = AttributeValue.objects.filter(attribute__name="size", product=product).order_by('value_option__order')

	# print(sizes)
	# print(variants)

	context = {
		'product': product,
		'sizes': sizes,
		'related_items': related_items,
	}
	

	template = 'product/product.html'

	return render(request, template, context)


