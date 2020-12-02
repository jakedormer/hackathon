from django.shortcuts import render

# Create your views here.

def hackathon_login(request):
	template = "hackathon/login.html"

	context = {
		'color': 'f8f9fa',
		'text': '212529'
	}

	return render(request, template, context)


def hackathon_welcome(request):
	template = "hackathon/welcome.html"

	context = {
		'color': 'f8f9fa',
		'text': '212529'
	}

	return render(request, template, context)

def hackathon_dashboard_bt(request):
	template = "hackathon/dashboard_bt.html"

	context = {
		'account': 'bt',
		'mrj': ['MRJ1', 'MRJ2', 'MRJ3'],
		'color': '563d7c',
		'text': 'fff',
		'rec': 'broadband deals',
		'images': [
			'https://content.presspage.com/uploads/633/1396020374121-3.png?10000',
			'https://shop.bt.com/images/product/uni2/DigitalContent/dy/DYNK_F78685DB-0FD1-44F1-BCE3-30AB9C8E61FD_large.jpg',
			'https://dam.which.co.uk/9888c1b3-ac0d-478f-b122-a732ddb36878.jpg'
			]
	}

	return render(request, template, context)

def hackathon_dashboard_ee(request):
	template = "hackathon/dashboard_ee.html"

	context = {
		'account': 'ee',
		'color': '007b85',
		'text': 'fff',
		'rec': 'sim only deals',
		'images': [
			'https://informitv.com/wordpress/wp-content/uploads/2019/11/BT-Sport.png',
			'https://www.metrofone.co.uk/shared/products/manufacturers/ee/EE-sim.png',
			'https://dam.which.co.uk/9888c1b3-ac0d-478f-b122-a732ddb36878.jpg',
			]
	}

	return render(request, template, context)