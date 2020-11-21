from django.contrib import admin
from django.urls import path, re_path, include
from apps.base import views as views_base
from apps.account import views as views_account
from apps.cart import views as views_cart
from apps.checkout import views as views_checkout
from apps.product import views as views_product
from apps.dashboard import views as views_dashboard
from apps.oauth import views as views_oauth
from apps.rest_api import views as views_rest_api
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from django.views.decorators.csrf import csrf_exempt

# router = routers.DefaultRouter()
# Users will be the name of the url

# router.register(r'groups', views.GroupViewSet)

# router.register(r'users', views_rest_api.UserViewSet)

urlpatterns = [

    # Base

    path('admin', admin.site.urls),
    path('', views_base.home, name='home'),
    path('about', views_base.about, name='about'),
    path('privacy', views_base.privacy, name='privacy'),
    path('bag', views_cart.cart, name='cart'),
    
    #Account
    path('account/orders', views_account.account_orders, name='account_orders'),
    path('account/favourites', views_account.account_favourites, name='account_favourites'),
    path('login', views_account.login_view, name='login'),
    path('login-vendor', views_account.login_vendor, name='login_vendor'),
    path('logout', views_account.logout_view, name='logout'),
    path('create-account', views_account.create_account, name='create_account'),

    # #Oauth
    # path('oauth/install', views_oauth.install, name='oauth/install'),
    # path('oauth/authenticate', views_oauth.authenticate, name='oauth/authenticate'),
    # path('<slug:slug>/c/<int:code>', views_product.category, name='category'),
    # re_path(r'.+/p/(?P<id>[0-9]+)', views_product.product, name='product'),

    # Cart
    path('add_to_cart', views_cart.add_to_cart, name='add_to_cart'),
    path('remove_from_cart', views_cart.remove_from_cart, name='remove_from_cart'),

    #Checkout
    path('checkout/login', views_checkout.checkout_login, name='checkout_login'),
    path('checkout/delivery', views_checkout.checkout_delivery, name='checkout_delivery'),

    # # Dashboard
    # path('dashboard', views_dashboard.dashboard, name='dashboard'),
    # path('dashboard/products', views_dashboard.dashboard_products, name='dashboard_products'),
    # path('dashboard/settings', views_dashboard.dashboard_settings, name='dashboard_settings'),
    # path('dashboard/sizes', views_dashboard.dashboard_sizes, name='dashboard_sizes'),
    # path('dashboard/sizes/delete/<int:code>', views_dashboard.dashboard_sizes_delete, name='dashboard_sizes_delete'),
    # path('dashboard/sizes/create', views_dashboard.dashboard_sizes_create, name='dashboard_sizes'),

    # Rest_API
    path('api/current_user/', views_rest_api.CurrentUser.as_view(), name='current_user'),
    path('api/update_vendor/', views_rest_api.Vendor.as_view(), name='update_vendor'),
    # path('api-token-auth/', obtain_auth_token, name='api_token_auth'),ss

    # Ajax
    # path('ajax/apply_size_guide', views_dashboard.apply_size_guide, name='apply_size_guide'),
    path('ajax/add_to_cart', views_cart.add_to_cart, name='add_to_cart'),
    path('ajax/add_to_favourites', views_account.add_to_favourites, name='favourite'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns 
