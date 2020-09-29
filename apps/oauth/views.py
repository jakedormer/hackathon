from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from apps.dashboard.models import Vendor, APICredential, Platform
import requests
import random
import string
import re
import urllib
import hmac as _hmac
import hashlib
from json import JSONDecodeError
import datetime
from django.views.decorators.clickjacking import xframe_options_exempt

def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result

def install(request):

	template 		= 'oauth/install.html'
	hostname 		= request.get_host()
	# print("hi, "+ request.get_host())
	# print(request.is_secure())

	if settings.DEBUG:
		protocol = "https://"
	else:
		if request.is_secure():

			protocol = "https://"
		else:
			protocol = "http://"

	print(protocol)

	redirect_uri 	= protocol + hostname + requests.utils.quote(settings.SHOPIFY_REDIRECT_URI)
	print(redirect_uri)

	# Shop must exist and have been created by admin else this process will fail.
	try:

		shop_url		= request.GET.get('shop')
		shop_name		= re.search(r'^([a-z\d_.]+)[.]myshopify[.]com[\/]?$', shop_url, re.IGNORECASE).group(1)

		# Try and find vendor. Name must be the name of the shopify store
		try:
			vendor = Vendor.objects.get(name=shop_name)
			
			# Add API Credentials with the nonce
			api_key 		= settings.SHOPIFY_API_KEY
			api_secret 		= settings.SHOPIFY_API_SECRET
			scopes 			= settings.SHOPIFY_API_SCOPES
			nonce 			= get_random_alphanumeric_string(49)
			
			print(redirect_uri)
			
			platform = Platform.objects.get(name="shopify")
			vendor_api_credentials, created = APICredential.objects.update_or_create(
				vendor=vendor,
				platform=platform,
				defaults = {
					'nonce': nonce,
					'scopes': scopes,
				}
			)



			install_url = "https://" + shop_name + ".myshopify.com/admin/oauth/authorize?client_id=" + api_key + "&scope=" + scopes + "&state=" + nonce + "&redirect_uri=" + redirect_uri

			return redirect(install_url)

		except ObjectDoesNotExist:

			messages.error(request, "Store must be created first, please contact the site owner to create a store on vestem.")

			return render(request, template)

	except (AttributeError, TypeError):

		messages.error(request, "Invalid install URL")
	
		return render(request, template)
	
	
def api_connect(vendor_name, endpoint, data):

    r = requests.post("https://" + vendor_name + endpoint, data=data)
    print(r.content)

    try:

        json_response = r.json()

        return [r.status_code, json_response]

    except JSONDecodeError:

        return [r.status_code, r.text]

@xframe_options_exempt
def authenticate(request):

	context = {}

	template = 'oauth/authenticate.html'

	# Get parameters from URL
	params = request.GET.dict()
	try:
		shop_url		= params['shop']
		context['shop'] = shop_url
		code			= params['code']
		hmac			= params['hmac']
		nonce			= params['state']

		# 1 Make sure shop name is correct format and that vendor exists in admin
		try:
			shop_name = re.search(r'^([a-z\d_.]+)[.]myshopify[.]com[\/]?$', shop_url, re.IGNORECASE).group(1)
			messages.success(request, "Shop name valid")
			security_pass_1 = True

			try:	
				vendor = Vendor.objects.get(name=shop_name)
				messages.success(request, "Vendor has been set up by our admin on vestem")
			
			except ObjectDoesNotExist:
				vendor = None
				messages.error(request, "Store must be created first, please contact the site owner to create a store on vestem.")

		except AttributeError:
			shop_name = None
			security_pass_1 = False
			messages.error(request, "Shop name invalid: " + shop_url)

	except KeyError:
		messages.error(request, "Invalid authenticate URL")
		security_pass_1 = False
		return render(request, template)

	#2 Check nonce is valid

	if shop_name and vendor:

		vendor_nonce = APICredential.objects.get(vendor=vendor, platform__name='shopify').nonce

		if nonce == vendor_nonce and len(nonce) == 49:

			messages.success(request, "Nonce key valid")
			security_pass_2 = True

		else:

			messages.error(request, "Nonce key invalid" )
			security_pass_2 = False

	else:

		messages.error(request, "Vendor and nonce key do not exist")
		security_pass_2 = False
			

	### 3. Check hmac is valid

	# Remove hmac from dict as per documentation and recombine into a query string
	cleaned_params = []
	for i in sorted(params):
	    if i in ['hmac']:
	        continue

	    cleaned_params.append((i, params[i]))

	# Recombine

	new_qs = urllib.parse.urlencode(cleaned_params, safe=":/")
	# print(new_qs)


	# Calculate the digest
	SECRET = settings.SHOPIFY_API_SECRET
	h = _hmac.new(SECRET.encode("utf8"), msg=new_qs.encode("utf8"), digestmod=hashlib.sha256)

	# Should return True if authenticated correctly

	verify = _hmac.compare_digest(h.hexdigest(), hmac)

	h = _hmac.new(SECRET.encode("utf8"), msg=new_qs.encode("utf8"), digestmod=hashlib.sha256)

	# print(h.hexdigest())
	# print(hmac)

	if verify:

		messages.success(request, "Oauth HMAC authentication valid")

		security_pass_3 = True

	else:

		messages.error(request, "Oauth HMAC authentication invalid")

		security_pass_3 = False

	print(security_pass_1, security_pass_2, security_pass_3)

	# If all security checks pass, then you can exchange the access code for a permanent access token

	api = api_connect(
		vendor_name = shop_name,
		endpoint=".myshopify.com/admin/oauth/access_token",
		data = {
			'client_id': settings.SHOPIFY_API_KEY,
			'client_secret': settings.SHOPIFY_API_SECRET,
			'code': code,
		})

	if api[0] == 200:

		try:

			APICredential.objects.update_or_create(
							vendor=vendor,
							platform__name='shopify',
							defaults = {
								'access_token': api[1]['access_token'],
								'scopes': api[1]['scope'],
							}
						)
			messages.success(request, "Access Token: Created successfully")

		except KeyError:

			messages.error(request, "Access Token: No JSON returned")

	else:
		messages.error(request, "Access token: API failed")
		print(api[0])
		context['html'] = api[1]

	
	# Now create a STOREFRONT access token:
	try:
		credential = APICredential.objects.get(vendor=vendor, platform__name="shopify")
		api_storefront = api_connect(
			vendor_name = shop_name,
			endpoint=".myshopify.com/admin/api/2020-07/storefront_access_tokens.json",
			data = {
				'title': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
				'access_token': credential.access_token,
				'access_scope': credential.scopes,
			})
	except ObjectDoesNotExist:

		messages.error(request, "Access Token: Object does not exist")

	if api_storefront[0] == 200:
			
		try:
			APICredential.objects.update_or_create(
							vendor=vendor,
							platform__name='shopify',
							defaults = {
								'access_token': api_storefront[1]['storefront_access_token']['access_token'],
							}
						)

			messages.success(request, "Storefront Access Token: Created successfully")

		except ObjectDoesNotExist:

			messages.error(request, "Storefront Access Token: Object does not exist")
	else:
		messages.error(request, "Storefront access token: API failed")
		
	

	return render(request, template, context)