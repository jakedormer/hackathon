from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from apps.dashboard.models import Vendor, APICredential
from apps.product.models import Product, Category, AttributeValue, Attribute
from apps.inventory.models import StockRecord
from apps.product.management.querys import update_products_shopify as q
import requests
from json import JSONDecodeError
import re


class Command(BaseCommand):
	help = "Update products in django database with products from shopify"



	def api_connect(self, vendor_name, access_token, endpoint, query):

		headers = {
				  'Accept': 'application/json',
				  'Content-Type': 'application/json',
				  # 'X-Shopify-Storefront-Access-Token': access_token,
				  'X-Shopify-Access-Token': access_token,
			  }


		# r = requests.post("https://" + vendor_name + ".myshopify.com/admin/api/2020-10/product_listings.json", json={'query': query}, headers=headers)
		r = requests.get("https://" + vendor_name + ".myshopify.com" + endpoint, headers=headers)

		try:

			json_response = r.json()
			# print(r.status_code)
			# print(json_response)
			# data = json_response['data']
			data = r.json()
			# print(data)
			# print(data)

			return [r.status_code, r.content, data]
			# return [r.status_code, r.json()]

		except JSONDecodeError:

			return [r.status_code, r.content, r.content]

	def regex_category(self, category):

		# T Shirts
		x = re.search(r'\b(tee|t[-\s]shirts?)\b', category, re.IGNORECASE)
		if x:
			return ["tops", "t-shirts"]

		# Shirts
		x = re.search(r'\b(shirts?)\b', category, re.IGNORECASE)
		if x:
			return ["tops", "shirts"]

		# Vests
		x = re.search(r'\b(vests?)\b', category, re.IGNORECASE)
		if x:
			return ["tops", "vests"]

		# Sweatshirts
		x = re.search(r'\b(sweatshirts?|jumpers?|fleeces?)\b', category, re.IGNORECASE)
		if x:
			return ["tops", "sweatshirts"]

	def regex_size(self, size):

		# X-Small
		if re.search(r'^xs$', size, re.IGNORECASE):
			return "XS"

		# Small
		if re.search(r'^s$', size, re.IGNORECASE):
			return "S"

		# Medium    
		if re.search(r'^m$', size, re.IGNORECASE):
			return "M"

		#Large
		if re.search(r'^l$', size, re.IGNORECASE):
			return "L"

		# X-Large
		if re.search(r'^xl$', size, re.IGNORECASE):
			return "XL"


	def update_products(self, json_data, vendor_id, graphql):

		# GraphQl Required manipulating the schema different to the sales channel API

		size_attr = Attribute.objects.get(name="size")

		if graphql == True:

			products = json_data['products']['edges']

			for product in products:
				p_title = product['node']['title']
				p_id = product['node']['id']
				p_category = product['node']['productType']
				p_external_url = product['node']['onlineStoreUrl']
				p_variants = product['node']['variants']['edges']

				try:
					p_image_src = node['node']['images']['edges'][0]['node']['originalSrc']

				# Product has no image
				except IndexError:
					p_image_src = None

		else:

			products = json_data['product_listings']
			# print(products)

			for product in products:
				# print(product)
				# print(product['product_id'])
				# print(product['title'])

				p_title = product['title']
				p_id = product['product_id']
				p_category = product['product_type']
				p_external_url = None
				p_variants = product['variants']

				try:

					p_image_src = product['images'][0]['src']

				except IndexError:
					p_image_src=None

				# print(p_image_src)

				# Create parents first and then create children. Children will have options and stock records.

				# Get category for foreignkey based on regex of title

				try:
					regex_category = self.regex_category(p_title)[1]

				except TypeError:
					regex_category = None

				try:
					category = Category.objects.get(name=regex_category)

				except ObjectDoesNotExist:

					category = None

				# print(category)

				# If 1 variant then item is standalone, else it is a parent

				if len(p_variants) == 1:
					
					product_type = "standalone"
				else:
					product_type = "parent"

				# print(product_type)

				p_obj, created = Product.objects.update_or_create(
					external_id=p_id,
					defaults = {
						'title': p_title, 
						'vendor_id': vendor_id, 
						'product_type': product_type,
						'category': category,
						'image_src': p_image_src,
						'external_url': p_external_url
						}
				)

				# print()

				# print(p_variants)
				print(len(p_variants))

				#Loop through variants
				for variant in p_variants:

					if graphql:
						v_title = variant['node']['title']
						v_code = variant['node']['id']
						v_price = variant['node']['price']
						v_quantity = variant['node']['quantityAvailable']
						v_options = variant['node']['selectedOptions']

					else:
						v_title = variant['title']
						v_code = variant['id']
						v_price = variant['price']
						v_quantity = variant['inventory_quantity']
						v_options = variant['option_values']

					# print(p_variants)
					# print(p_title)

					print(variant)
					# print(forloop.counter())

					# Sieve through options to find size variable
					for i in v_options:

						try:
							if re.search(r'\b(size|sizing)\b', i['name'], re.IGNORECASE):

								size = self.regex_size(i['value'])

								break

							else:
								size = None

						# If null is returned

						except TypeError:

							print("typerror")

					print('size', size)

					# Create a standalone stock record and size attribute value
					if product_type == "standalone":

						i_obj, created = StockRecord.objects.update_or_create(
							product=p_obj,
							defaults = {
								'price_inc_tax': v_price,
								'num_in_stock': v_quantity,
							})


						if size:
							# Create size attribute value

							a_obj, created = AttributeValue.objects.update_or_create(
								attribute=size_attr,
								product=p_obj,
								defaults = {
									'value_text': size,
								})

							print(created)

					# Create a parent product, variant, size attribute value and variant stock records
					else:
						# Create variant product
						c_obj, created = Product.objects.update_or_create(
							external_id=v_code,
							defaults = {
								'title':v_title, 
								'vendor_id': vendor_id, 
								'product_type': "variant",
								'parent': p_obj,
								}
						)

						# Create stock record for variant
						cs_obj, created = StockRecord.objects.update_or_create(
							product=c_obj,
							defaults = {
								'price_inc_tax': v_price,
								'num_in_stock': v_quantity,
							})

						if size:
							# Create size attribute value for variant
							size_attr = Attribute.objects.get(name="size")

							a_obj, created = AttributeValue.objects.update_or_create(
								attribute=size_attr,
								product=c_obj,
								defaults = {
									'value_text': size,
								})


	def handle(self, *args, **options):

		vendors = Vendor.objects.all()

		for vendor in vendors:

			try:
				
				api_credential = APICredential.objects.get(vendor=vendor, platform__name='shopify')
				# print(api_credential.platform.sales_channel_endpoint)

				p = self.api_connect(vendor_name=vendor.name, access_token=api_credential.access_token, endpoint=api_credential.platform.sales_channel_endpoint, query=q.query)

				if p[0] == 200:
					print("API connected successfully")
					# print(p[1])
					self.update_products(json_data=p[2], vendor_id=vendor.id, graphql=False)
					print("Product created")
				else:
					print("API unsuccessful")
					print(p)



			except ObjectDoesNotExist:

				pass

			
	def update_products_sales_channel(self):

		return



			
		