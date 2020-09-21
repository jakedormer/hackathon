from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from apps.dashboard.models import Vendor, APICredential
import requests
import random
import string
import re
import urllib
import hmac as _hmac
import hashlib

def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result

def install(request):

	shop_url		= request.GET.get('shop')

	shop_name		= re.search(r'^([a-z\d_.]+)[.]myshopify[.]com[\/]?$', shop_url, re.IGNORECASE).group(1)
	api_key 		= settings.SHOPIFY_API_KEY
	api_secret 		= settings.SHOPIFY_API_SECRET
	scopes 			= settings.SHOPIFY_API_SCOPES
	nonce 			= get_random_alphanumeric_string(49)
	redirect_uri 	= requests.utils.quote(settings.SHOPIFY_REDIRECT_URI)

	install_url = "https://" + shop_name + ".myshopify.com/admin/oauth/authorize?client_id=" + api_key + "&scope=" + scopes + "&state=" + nonce + "&redirect_uri=" + redirect_uri

	# Create a vendor if none exists
	vendor, created = Vendor.objects.get_or_create(name=shop_name)
	
	# Add API Credentials with the nonce
	vendor_api_credentials, created = APICredential.objects.update_or_create(
		vendor=vendor,
		platform__name='shopify',
		defaults = {
			'nonce': nonce,
			'scopes': scopes,
		}
	)

	print("hello")
	template = 'oauth/install.html'

	return redirect(install_url)



def authenticate(request):

	template = 'oauth/authenticate.html'

	# Get parameters from URL
	params = request.GET.dict()
	print(params)

	shop_url		= params['shop']
	shop_name		= re.search(r'^([a-z\d_.]+)[.]myshopify[.]com[\/]?$', shop_url, re.IGNORECASE).group(1)
	code			= params['code']
	hmac			= params['hmac']
	nonce			= params['state']

	### 1. Check shop name matches the regular expression

	if re.search(r'^([a-z\d_.])+[.]myshopify[.]com[\/]?$', shop_url):

		messages.success(request, "Shop name valid")

		security_pass_1 = True
		
	else:

		security_pass_1 = False
		messages.error(request, "Shop name invalid: " + shop_url)

	### 2. Check nonce is equal to original nonce
	vendor = Vendor.objects.get(name=shop_name)
	vendor_nonce = APICredential.objects.get(vendor=vendor, platform__name='shopify').nonce

	if nonce == vendor_nonce and len(nonce) == 49:

		messages.success(request, "Nonce key valid")
		security_pass_2 = True

	else:

		messages.error(request, "Nonce key invalid")
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
	print(new_qs)


	# Calculate the digest
	SECRET = settings.SHOPIFY_API_SECRET
	h = _hmac.new(SECRET.encode("utf8"), msg=new_qs.encode("utf8"), digestmod=hashlib.sha256)

	# Should return True if authenticated correctly

	verify = _hmac.compare_digest(h.hexdigest(), hmac)

	h = _hmac.new(SECRET.encode("utf8"), msg=new_qs.encode("utf8"), digestmod=hashlib.sha256)

	print(h.hexdigest())
	print(hmac)

	if verify:

		messages.success(request, "Oauth HMAC authentication passed")

		security_pass_3 = True

	else:

		messages.error(request, "Oauth HMAC authentication invalid")

		security_pass_3 = False




	print(security_pass_1, security_pass_2, security_pass_3)

	
	print(verify)




	return render(request, template, {})