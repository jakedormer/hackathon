import string
import random

class CartMiddleware:

	def get_random_alphanumeric_string(self, length):
		letters_and_digits = string.ascii_letters + string.digits
		result = ''.join((random.choice(letters_and_digits) for i in range(length)))
		return result

	def __init__(self, get_response):
		self.get_response = get_response
		# One-time configuration and initialization.

	def __call__(self, request):
		# Code to be executed for each request before
		# the view (and later middleware) are called.

		response = self.get_response(request)


		if request.COOKIES.get('session_key'):

			# print("Has cookie")
			pass

		else:

			response.set_cookie(
				'session_key', 
				value=self.get_random_alphanumeric_string(64),
				expires=None, 
				max_age=60*60*24*30,
				domain='127.0.0.1',

			)

		# Code to be executed for each request/response after
		# the view is called.

		return response



	#     # Code to be executed for each request/response after
	#     # the view is called.
