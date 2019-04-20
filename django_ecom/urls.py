"""django_ecom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import  url
from django.contrib import admin
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from products.views import ProductListView,\
    ProductDetailView,ProductFeaturedListView,ProductFeaturedDetailView
from carts.views import cart


urlpatterns = [
    url(r'^admin/',admin.site.urls),
    url(r'^accounts/', include("accounts.urls", namespace='accounts')),
    url(r'^cart/', include("carts.urls", namespace='carts')),
    url(r'^$',ProductListView.as_view(), name='productlist'),
    path('featured', ProductFeaturedListView.as_view(), name='featured_list'),
    path('products/<slug:slug>', ProductDetailView.as_view(), name='productdetail'),
    url(r'^featured/(?P<slug>\d+)/$',ProductFeaturedDetailView.as_view())

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



