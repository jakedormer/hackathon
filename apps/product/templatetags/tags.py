from django import template
from apps.product.models import Product

register = template.Library()

@register.filter(name="get_item")
def get_item(dictionary, key):
    return dictionary.get(key)

@register.inclusion_tag('../templates/product/product_card.html')
def product_card(product_id):

    return {
    	'product': Product.objects.filter(id=product_id).first()
    }