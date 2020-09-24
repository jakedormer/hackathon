from django.shortcuts import render

from django.views.decorators.clickjacking import xframe_options_exempt

# Create your views here.

@xframe_options_exempt
def home(request):
	context = locals()
	template = 'home.html'

	return render(request,template,context)

@xframe_options_exempt
def about(request):
	context = locals()
	template = 'about.html'

	return render(request,template,context)


def privacy(request):
	context = locals()
	template = 'privacy.html'

	return render(request,template,context)