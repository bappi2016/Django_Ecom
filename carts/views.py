from django.shortcuts import render,get_object_or_404,redirect,reverse
from .models import Cart
from products.models import Product
from django.conf import settings


def cart(request): # session will get cart when the url is being requested
    cart_obj,new_obj = Cart.objects.get_cart_or_create(request) # create two instance with the same name as refer to the get_cart_or_create with the parent model class Cart -the method belong to Cart now
    products = cart_obj.products.all() #will returns the list of products. product is the many to many model field- here we did this for testing purpose
    total = 0
    for item in products:
        total += item.price # price is the attribute of Cart model
    # print(total)
    cart_obj.total = total
    cart_obj.save()

    return render(request,'carts/cart_home.html',{'cart':cart_obj})

