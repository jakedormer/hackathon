from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from apps.dashboard.models import Vendor, APICredential
from apps.product.models import Product, Category
from apps.inventory.models import StockRecord
from apps.product.management.querys import update_products_shopify as q
import requests
from json import JSONDecodeError
import re


class Command(BaseCommand):
    help = "Update products in django database with products from shopify"



    def api_connect(self, vendor_name, access_token, query):

        headers = {
                  'Accept': 'application/json',
                  'Content-Type': 'application/json',
                  'X-Shopify-Storefront-Access-Token': access_token,
              }


        r = requests.post("https://" + vendor_name + ".myshopify.com/api/2020-07/graphql", json={'query': query}, headers=headers)

        try:

            json_response = r.json()
            # print(r.status_code)
            # print(json_response)
            data = json_response['data']
            # print(data)

            return [r.status_code, data]

        except JSONDecodeError:

            return [r.status_code, r.text]

    def regex_category(self, category):

        #T Shirts
        x = re.search(r'\b(tee|t[-\s]shirts?)\b', category, re.IGNORECASE)
        if x:
            return "t-shirts"

        #Shirts
        x = re.search(r'\b(shirts?)\b', category, re.IGNORECASE)
        if x:
            return "shirts"

        #Vests
        x = re.search(r'\b(vests?)\b', category, re.IGNORECASE)
        if x:
            return "vests"


    def update_products(self, json_data, vendor_id):

        products = json_data['products']['edges']
        # print(products)

        # Create parents first and then create children. Children will have options and stock records.

        for node in products:
            p_title = node['node']['title']
            p_code = node['node']['id']
            p_category = node['node']['productType']
            p_external_url = node['node']['onlineStoreUrl']
            # print(p_category)
            p_variants = node['node']['variants']['edges']
            p_image_src = node['node']['images']['edges'][0]['node']['originalSrc']
            # print(p_image_src)
            # print(len(p_variants))

            # Get category for foreignkey base don regex of title

            try:
                regex_category = self.regex_category(p_title)
                category = Category.objects.get(name=regex_category)

            except ObjectDoesNotExist:
                category = None

            # If 1 variant then item is standalone, else it is a parent

            if len(p_variants) == 1:
                product_type = "standalone"
            else:
                product_type = "parent"

            # Create product for standalone and parent
            p_obj, created = Product.objects.update_or_create(
                id=p_code,
                defaults = {
                    'title':p_title, 
                    'vendor_id': vendor_id, 
                    'product_type': product_type,
                    'category': category,
                    'image_src': p_image_src,
                    'external_url': p_external_url
                    }
            )

            #Loop through variants
            for node in p_variants:
                c_title = node['node']['title']
                c_code = node['node']['id']
                c_price = node['node']['price']
                c_quantity = node['node']['quantityAvailable']
                c_options = node['node']['selectedOptions']

                # Create a standalone stock record
                if product_type == "standalone":

                    i_obj, created = StockRecord.objects.update_or_create(
                        product=p_obj,
                        defaults = {
                            'price_inc_tax': c_price,
                            'num_in_stock': c_quantity,
                        })

                # Create a parent product, child and child stock records
                else:

                    # Create child product
                    c_obj, created = Product.objects.update_or_create(
                        id=c_code,
                        defaults = {
                            'title':c_title, 
                            'vendor_id': vendor_id, 
                            'product_type': "child",
                            'parent': p_obj,
                            }
                    )
                    # Create stock record for child
                    i_obj, created = StockRecord.objects.update_or_create(
                        product=c_obj,
                        defaults = {
                            'price_inc_tax': c_price,
                            'num_in_stock': c_quantity,
                        })


    def handle(self, *args, **options):

        vendors = Vendor.objects.all()

        for vendor in vendors:

            try:
                
                api_credential = APICredential.objects.get(vendor=vendor, platform__name='shopify')

                p = self.api_connect(vendor_name=vendor.name, access_token=api_credential.access_token, query=q.query)

                if p[0] == 200:
                    print("API connected successfully")
                    print(p[1])
                    self.update_products(json_data=p[1], vendor_id=vendor.id)
                    print("Product created")
                else:
                    print("API unsuccessful")
                    print(p)



            except ObjectDoesNotExist:

                pass

            




            
        