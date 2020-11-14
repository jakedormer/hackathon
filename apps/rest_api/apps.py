from django.apps import AppConfig


class RestApiConfig(AppConfig):
    name = 'apps.rest_api'

    def ready(self):
    	import apps.rest_api.signals
