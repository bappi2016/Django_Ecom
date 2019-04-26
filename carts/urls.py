from django.conf.urls import  url
from .views import cart
from products.views import update_cart,checkout_home

app_name = 'cart'

urlpatterns = [
 url(r'^$',cart,name='cart'),
 url(r'^updatecart/$',update_cart,name='updatecart'),
 url(r'^checkout/$',checkout_home,name='checkout'),


]