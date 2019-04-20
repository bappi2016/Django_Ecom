from django.conf.urls import  url
from .views import cart
from products.views import update_cart

app_name = 'cart'

urlpatterns = [
 url(r'^$',cart,name='cart'),
 url(r'^/updatecart/$',update_cart,name='updatecart'),


]