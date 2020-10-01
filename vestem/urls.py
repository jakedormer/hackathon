"""vestem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from views import base
from apps.cart import views as views_cart
from apps.product import views as views_product
from apps.dashboard import views as views_dashboard
from apps.oauth import views as views_oauth
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin', admin.site.urls),
    path('', base.home, name='home'),
    path('about', base.about, name='about'),
    path('privacy', base.privacy, name='privacy'),
    path('cart', views_cart.cart, name='cart'),
    path('login', views_dashboard.login_view, name='login'),
    path('logout', views_dashboard.logout_view, name='logout'),
    path('oauth/install', views_oauth.install, name='oauth/install'),
    path('oauth/authenticate', views_oauth.authenticate, name='oauth/authenticate'),
    path('c/<slug:slug>', views_product.category, name='category'),
    path('p/<slug:slug>', views_product.product, name='product'),
    path('dashboard', views_dashboard.dashboard, name='dashboard'),
    path('dashboard/products', views_dashboard.dashboard_products, name='dashboard_products'),
    path('dashboard/settings', views_dashboard.dashboard_settings, name='dashboard_settings'),
    path('dashboard/sizes', views_dashboard.dashboard_sizes, name='dashboard_sizes'),
    path('dashboard/sizes/delete/<int:code>', views_dashboard.dashboard_sizes_delete, name='dashboard_sizes_delete'),
    path('dashboard/sizes/create', views_dashboard.dashboard_sizes_create, name='dashboard_sizes'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns 
