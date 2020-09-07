from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from apps.dashboard.models import Vendor, APICredential
from apps.product.models import Product
from apps.product.management.querys import update_products_shopify as q
import requests
from json import JSONDecodeError


class Command(BaseCommand):
    help = "Update products in django database with products from shopify"



    def api_connect(self, vendor_name, access_token, query):

        headers = {
                  'Accept': 'application/json',
                  'Content-Type': 'application/json',
                  'X-Shopify-Storefront-Access-Token': access_token,
              }


        r = requests.post("https://" + vendor_name + ".myshopify.com/api/2020-04/graphql", json={'query': query}, headers=headers)

        try:

            json_response = r.json()
            # print(r.status_code)

            data = json_response['data']
            # print(data)

            return [r.status_code, data]

        except JSONDecodeError:

            return [r.status_code, r.text]

    def update_products(self, json_data, vendor_id):

        products = json_data['products']['edges']

        for edges in products:
            title = edges['node']['title']
            code = edges['node']['id']
            print(code)

            obj, created = Product.objects.update_or_create(code=code, title=title, vendor_id=vendor_id, product_type="parent")


    def handle(self, *args, **options):

        vendors = Vendor.objects.all()

        for vendor in vendors:

            try:
                
                api_credential = APICredential.objects.get(vendor=vendor, platform__name='shopify')

                p = self.api_connect(vendor_name=vendor.name, access_token=api_credential.access_token, query=q.query)

                if p[0] == 200:
                    print("API connected successfully")
                    # print(p[1])
                    self.update_products(json_data=p[1], vendor_id=vendor.id)
                    print("Product created")
                else:
                    print("API unsuccessful")
                    print(p)



            except ObjectDoesNotExist:

                pass

            




            
        